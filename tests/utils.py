"""TEST - UTILS
Misc helpers/utils functions for tests
"""

# # Native # #
from datetime import datetime
from random import randint

# # Project # #
from users_api.models import *
from users_api.repositories import UsersRepository
from users_api.utils import get_uuid

__all__ = (
    "get_user_create", "get_existing_user",
    "get_uuid"
)


def get_address(**kwargs):
    return Address(**{
        "street": get_uuid(),
        "city": get_uuid(),
        "state": get_uuid(),
        "zip_code": randint(1000, 10000),
        **kwargs
    })


def get_user_create(**kwargs):
    return UserCreate(**{
        "name": get_uuid(),
        "address": get_address(),
        "birth": datetime.now().date(),
        **kwargs
    })


def get_existing_user(**kwargs):
    return UsersRepository.create(get_user_create(**kwargs))
