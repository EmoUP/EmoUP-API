"""MODELS - USER ADDRESS
The address of a user is part of the User model
"""

# # Package # #
from .common import BaseModel
from .fields import AddressFields

__all__ = ("Address",)


class Address(BaseModel):
    """The address information of a user"""
    street: str = AddressFields.street
    city: str = AddressFields.city
    state: str = AddressFields.state
    zip_code: str = AddressFields.zip_code
