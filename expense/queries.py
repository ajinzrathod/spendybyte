from account.models import Account
from django.db.models import Q


GRANT_SUPERUSER = True
active_superuser = Q()

if GRANT_SUPERUSER:
    active_superuser = Q(is_active=True, is_superuser=True)

# start queries from here
users_with_update_access_to_expense_app = Account.objects.filter(
    active_superuser | Q(user_permissions__codename="change_expense")
).distinct()
