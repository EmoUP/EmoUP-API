"""MODELS - MUSIC
The Music model
"""

# # Package # #
from .common import BaseModel
from .fields import MusicFields
from .music_update import MusicUpdate

__all__ = ("MusicCreate",)


class MusicCreate(MusicUpdate):
    """The information of a Music"""
    name: str = MusicFields.name
    url: str = MusicFields.url
    