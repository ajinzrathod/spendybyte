from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.sessions.models import Session

from django.utils.translation import gettext_lazy as _

from account.models import Account


@admin.display(description="Id")
def id(obj):
    return str("{:04d}".format(obj.id))


@admin.display(description="Full Name")
def full_name(obj):
    return "%s %s" % (obj.first_name, obj.last_name)


class AccountAdminConfig(UserAdmin):
    readonly_fields = ("last_modified", "date_joined", "last_login")
    ordering = ("-date_joined",)
    list_display = (
        id,
        "username",
        "email",
        full_name,
        "is_active",
    )
    list_filter = (
        "is_active",
        "is_staff",
        "is_superuser",
    )
    fieldsets = (
        (
            None,
            {"classes": ("wide",), "fields": ("username", "password")},
        ),
        (
            "Personal Info",
            {
                "fields": (
                    ("first_name", "last_name"),
                    "email",
                    "gender",
                    "date_of_birth",
                )
            },
        ),
        (
            "Fundamental Permissions",
            {
                "classes": ("wide",),
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
        (
            "Group Permissions",
            {
                "classes": ("collapse",),
                "fields": (
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            "Important Dates",
            {
                "classes": ("wide",),
                "fields": (("date_joined", "last_modified", "last_login"),),
            },
        ),
        (
            "User Settings",
            {
                "classes": ("wide",),
                "fields": ("prefered_time_zone",),
            },
        ),
    )

    empty_value_display = "--"

    actions = ["mark_as_active"]

    def mark_as_active(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, _("Selected users marked as active."))

    mark_as_active.short_description = _("Mark selected users as active")


class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()

    list_display = ["session_key", "_session_data", "expire_date"]


admin.site.register(Session, SessionAdmin)
admin.site.register(Account, AccountAdminConfig)
