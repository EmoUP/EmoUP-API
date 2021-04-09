"""MODELS - MUSIC - READ
Music Read model. Inherits from MusicCreate and adds the music_id field, which is the _id field on Mongo documents
"""

# # Native # #
from datetime import datetime
from typing import Optional, List

# # Installed # #
import pydantic
from dateutil.relativedelta import relativedelta

# # Package # #
from .music_create import MusicCreate
from .fields import MusicFields

__all__ = ("MusicRead", "MusicsRead")


class MusicRead(MusicCreate):
    """Body of Music GET and POST responses"""
    music_id: str = MusicFields.music_id
    created: int = MusicFields.created
    updated: int = MusicFields.updated

    @pydantic.root_validator(pre=True)
    def _set_music_id(cls, data):
        """Swap the field _id to music_id (this could be done with field alias, by setting the field as "_id"
        and the alias as "music_id", but can be quite confusing)"""
        document_id = data.get("_id")
        if document_id:
            data["music_id"] = document_id
        return data

    class Config(MusicCreate.Config):
        extra = pydantic.Extra.ignore  # if a read document has extra fields, ignore them


MusicsRead = List[MusicRead]
