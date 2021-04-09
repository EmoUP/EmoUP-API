"""MODELS - USER EMOTION
The emotion of a user is part of the User model
"""

# # Package # #
from .common import BaseModel
from .fields import StateFields

__all__ = ("Emotion",)


class Emotion(BaseModel):
    """The emotion state information of a user"""
    emotion: str = StateFields.emotion
    captured: int = StateFields.captured