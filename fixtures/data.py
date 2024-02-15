# import datetime
# from account.gender import MALE
# from account.models import Account
# from expense.approval_status import PENDING
# from expense.models import Expense

# get_dummy_account = Account(
#     username="johndoe",
#     first_name="John",
#     last_name="Doe",
#     email="johndoe@example.com",
#     gender=MALE,
#     date_of_birth=datetime.date(1970, 1, 30),
#     is_active=True,
#     is_staff=False,
#     is_superuser=False,
#     prefered_time_zone="Asia/Kolkata",
# )

# get_dummy_supervisor_account = Account(
#     username="ajinzrathod",
#     first_name="Ajinkya",
#     last_name="Rathod",
#     email="ajinzrathod@example.com",
#     gender=MALE,
#     date_of_birth=datetime.date(1999, 1, 26),
#     is_active=True,
#     is_staff=True,
#     is_superuser=True,
#     prefered_time_zone="Asia/Kolkata",
# )

# get_dummy_expense_with_pending_approval = Expense(
#     requested_by=get_dummy_account,
#     expense_amount=1000,
#     expense_title="Home Office Fund",
#     expense_description="Monitor and Chair",
#     receipt="dummy/path/to/receipt.jpg",
#     approval_status=PENDING,
#     approved_by=None,
# )
