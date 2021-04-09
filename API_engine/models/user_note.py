"""MODELS - USER NOTE
The note of a user is part of the User model
"""

# # Package # #
from .common import BaseModel
from .fields import NoteFields

__all__ = ("Note",)


class Note(BaseModel):
    """The notes of a user"""
    note: str = NoteFields.note
    color: str = NoteFields.color
    captured: str = NoteFields.captured