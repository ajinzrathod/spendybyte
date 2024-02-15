from django.db import models
from django.apps import apps
from django.utils.translation import gettext_lazy as _
import pytz
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.contrib.auth.hashers import make_password
from django.core.cache import cache

from account.gender import GENDERS, UNSPECIFIED
from account.validators import UnicodeUsernameValidator


class AccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError("The given username must be set")
        if not email:
            raise ValueError("You must provide an email address")

        # Lowercasing the domain part
        email = self.normalize_email(email)

        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(
        self, username, email=None, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin):
    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))

    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _("username"),
        # editable=False,
        max_length=30,
        unique=True,
        db_index=True,
        help_text=_(
            "Readonly. Required. 150 characters or fewer."
            # 'Letters, digits and @/./+/-/_ only.'),
            "Letters, digits, dots and underscores only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    # password

    # Personal Info
    first_name = models.CharField(_("first name"), max_length=150, blank=True)

    last_name = models.CharField(_("last name"), max_length=150, blank=True)

    email = models.EmailField(_("email address"), db_index=True)

    gender = models.CharField(
        _("gender"),
        max_length=20,
        choices=GENDERS,
        default=UNSPECIFIED,
    )

    # blank=True (for the admin) and null=True (for the database).
    date_of_birth = models.DateField(_("Date of Birth"), blank=True, null=True)

    # Permissions
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "States whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("States whether the user can log into this admin site."),
    )
    is_superuser = models.BooleanField(
        _("superuser status"),
        default=False,
        help_text=_(
            "States that this user has all permissions without "
            "explicitly assigning them."
        ),
    )

    # User permission according to group

    # Important Dates
    date_joined = models.DateTimeField(_("date joined"), auto_now_add=True)
    last_modified = models.DateTimeField(_("date modified"), auto_now=True)

    prefered_time_zone = models.CharField(
        max_length=32, choices=TIMEZONES, default="Asia/Kolkata"
    )

    objects = AccountManager()

    EMAIL_FIELD = "email"

    # Login field
    USERNAME_FIELD = "username"

    # Must be specified while creating superuser
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = _("Account")
        verbose_name_plural = _("Accounts")

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        # Set is_active to False by default if it's not already set
        # Check if the user is being created (not already saved)
        if self.pk is None and self.is_staff is False:
            self.is_active = False

        if self.pk:
            old_instance = Account.objects.get(pk=self.pk)
            if self.prefered_time_zone != old_instance.prefered_time_zone:
                cache.delete(f"user_timezone_{self.id}")
        super().save(*args, **kwargs)
