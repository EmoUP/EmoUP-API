"""MODELS - USER DEEPFAKE
The deepfake of a user is part of the User model
"""


# # Native # #
from typing import Optional

# # Package # #
from .common import BaseModel
from .fields import DeepFakeFields

__all__ = ("DeepFake",)


class DeepFake(BaseModel):
    """The deepfake information of a user"""
    name: Optional[str] = DeepFakeFields.name
    image: Optional[str] = DeepFakeFields.image
    voice: Optional[str] = DeepFakeFields.voice
    output: Optional[str] = DeepFakeFields.output
