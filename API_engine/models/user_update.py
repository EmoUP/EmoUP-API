"""MODELS - USER - UPDATE
User Update model. All attributes are set as Optional, as we use the PATCH method for update
(in which only the attributes to change are sent on request body)
"""

# # Native # #
from datetime import date
from typing import Optional, List
from contextlib import suppress

# # Package # #
from .common import BaseModel
from .fields import UserFields
from .user_address import Address
from .user_emotion import Emotion
from .user_deepfakes import DeepFake

__all__ = ("UserUpdate",)


class UserUpdate(BaseModel):
    """Body of User PATCH requests"""
    name: Optional[str] = UserFields.name
    password: Optional[str] = UserFields.password
    address: Optional[Address] = UserFields.address_update
    states: Optional[List[Emotion]] = UserFields.states
    deepfake: Optional[DeepFake] = UserFields.deepfake
    birth: Optional[date] = UserFields.birth
    profile_pic: Optional[str] = UserFields.profile_pic
    current_emotion: Optional[str] = UserFields.current_emotion

    def dict(self, **kwargs):
        # The "birth" field must be converted to string (isoformat) when exporting to dict (for Mongo)
        # TODO Better way to do this? (automatic conversion can be done with Config.json_encoders, but not available for dict
        d = super().dict(**kwargs)
        with suppress(KeyError):
            d["birth"] = d.pop("birth").isoformat()    
        return d
