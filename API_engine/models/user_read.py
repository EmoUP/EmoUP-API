"""MODELS - USER - READ
User Read model. Inherits from UserCreate and adds the user_id field, which is the _id field on Mongo documents
"""

# # Native # #
from datetime import datetime
from typing import Optional, List

# # Installed # #
import pydantic
from dateutil.relativedelta import relativedelta

# # Package # #
from .user_create import UserCreate
from .fields import UserFields

__all__ = ("UserRead", "UsersRead")


class UserRead(UserCreate):
    """Body of User GET and POST responses"""
    user_id: str = UserFields.user_id
    age: Optional[int] = UserFields.age
    created: int = UserFields.created
    updated: int = UserFields.updated

    @pydantic.root_validator(pre=True)
    def _set_user_id(cls, data):
        """Swap the field _id to user_id (this could be done with field alias, by setting the field as "_id"
        and the alias as "user_id", but can be quite confusing)"""
        document_id = data.get("_id")
        if document_id:
            data["user_id"] = document_id
        return data

    @pydantic.root_validator()
    def _set_age(cls, data):
        """Calculate the current age of the user from the date of birth, if any"""
        birth = data.get("birth")
        if birth:
            today = datetime.now().date()
            data["age"] = relativedelta(today, birth).years
        return data

    class Config(UserCreate.Config):
        extra = pydantic.Extra.ignore  # if a read document has extra fields, ignore them


UsersRead = List[UserRead]
