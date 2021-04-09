"""MODELS - USER - CREATE
User Create model. Inherits from UserUpdate, but all the required fields must be re-defined
"""

# # Package # #
from .user_update import UserUpdate
from .user_address import Address
from .fields import UserFields

__all__ = ("UserCreate",)


class UserCreate(UserUpdate):
    """Body of User POST requests"""
    name: str = UserFields.name
    email: str = UserFields.email
    password: str = UserFields.password
    