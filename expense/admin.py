from django.contrib import admin

from expense.queries import users_with_update_access_to_expense_app
from expense.models import Expense


# when number has less digits, it was hard to click
@admin.display(description="ID")
def id(obj):
    return str("{:04d}".format(obj.id))


class ExpenseAdmin(admin.ModelAdmin):
    search_fields = (
        "requested_by__email",
        "requested_by__username",
        "requested_by__first_name",
        "requested_by__last_name",
    )
    autocomplete_fields = ("requested_by",)

    ordering = ("-created_at",)
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    list_display = (
        id,
        "requested_by",
        "expense_amount",
        "expense_title",
        "approval_amount",
        "approval_status",
        "approved_by",
        "created_at",
        "updated_at",
    )
    fields = (
        "requested_by",
        "expense_amount",
        "expense_title",
        "expense_description",
        "receipt",
        "approval_amount",
        "approval_status",
        "approved_by",
        "created_at",
        "updated_at",
    )

    list_filter = ("approval_status",)

    # we cant use use raw_id_fields on approved_by else
    # the custom queryset would have no point, and any user can be selected
    raw_id_fields = ("requested_by",)

    # approved by will only show those users
    # who have access to change expense app
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "approved_by":
            custom_queryset = users_with_update_access_to_expense_app
            kwargs["queryset"] = custom_queryset
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Expense, ExpenseAdmin)
