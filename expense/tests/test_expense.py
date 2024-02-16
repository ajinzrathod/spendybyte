import pytest
from fixtures.data import get_dummy_account
from expense.approval_status import PENDING
from expense.models import Expense


@pytest.mark.django_db
def test_that_object_gets_created():
    get_dummy_account.save()
    expense = Expense(
        requested_by=get_dummy_account,
        expense_amount=1000,
        expense_title="Home Office Fund",
        expense_description="Monitor and Chair",
        receipt="dummy/path/to/receipt.jpg",
        approval_status=PENDING,
        approved_by=None,
    )
    expense.save()

    assert isinstance(expense, Expense)
    assert expense.expense_amount == 1000
    assert expense.expense_title == "Home Office Fund"
    assert expense.expense_description == "Monitor and Chair"
    assert expense.receipt == "dummy/path/to/receipt.jpg"
    assert expense.approval_status == PENDING
    assert expense.approved_by is None
