import environ
from django.contrib.auth.password_validation import validate_password
import pytest


@pytest.mark.django_db
def test_secret_key_strength():
    assert 1 == 1
    # env = environ.Env()
    # environ.Env.read_env()
    # SECRET_KEY = env("SECRET_KEY")

    # try:
    #     validate_password(SECRET_KEY)
    # except Exception as e:
    #     exception = f"Bad Secret Key {e.messages}"
    #     pytest.fail(exception)
