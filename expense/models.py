from datetime import datetime
import os
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator

from account.models import Account

from expense.approval_status import APPROVAL_STATUS, PENDING
from expense.validators import validate_max_file_size
from spendybyte.common import BYTE_SIZE_5_MB
from functools import partial
from django.core.exceptions import ValidationError


validate_file_size = partial(validate_max_file_size, max_size=BYTE_SIZE_5_MB)


def get_upload_path(instance, filename):
    return os.path.join("receipts", datetime.now().strftime("%Y/%m"), filename)


class Expense(models.Model):
    requested_by = models.ForeignKey(
        Account,
        on_delete=models.RESTRICT,
        related_name="requested_by",
        blank=True,
        null=True,
    )
    expense_amount = models.DecimalField(max_digits=10, decimal_places=2)
    expense_title = models.CharField(max_length=60)
    expense_description = models.CharField(max_length=300, blank=True)

    receipt = models.FileField(
        upload_to=get_upload_path,
        validators=[
            FileExtensionValidator(
                allowed_extensions=["pdf", "jpg", "jpeg", "png", "xlsx", "xls"]
            ),
            validate_file_size,
        ],
    )
    approval_amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )

    approval_status = models.CharField(
        max_length=20,
        choices=APPROVAL_STATUS,
        default=PENDING,
    )

    approved_by = models.ForeignKey(
        Account,
        on_delete=models.RESTRICT,
        blank=True,
        null=True,
        related_name="approved_by",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.approval_amount > self.expense_amount:
            raise ValidationError(
                {
                    "approval_amount": "Approval amount cannot be greater than expense amount."
                }
            )

        if self.approval_status != PENDING and not self.approved_by:
            raise ValidationError(
                {
                    "approved_by": "The 'Approved by' field cannot be left empty unless the approval status is 'Pending'."
                }
            )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(
                    approval_status__in=[
                        choice[0] for choice in APPROVAL_STATUS
                    ]
                ),
                name="valid_status_constraint",
            )
        ]

        verbose_name = _("Expense")
        verbose_name_plural = _("Expenses")
