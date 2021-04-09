"""MODELS - MUSIC - UPDATE
Music Update model. All attributes are set as Optional, as we use the PATCH method for update
(in which only the attributes to change are sent on request body)
"""

# # Native # #
from datetime import date
from typing import Optional, List
from contextlib import suppress

# # Package # #
from .common import BaseModel
from .fields import MusicFields

__all__ = ("MusicUpdate",)


class MusicUpdate(BaseModel):
    """Body of Music PATCH requests"""
    name: Optional[str] = MusicFields.name
    url: Optional[str] = MusicFields.url
    cluster: Optional[str] = MusicFields.cluster
    counts: Optional[List[str]] = MusicFields.counts
    number_of_likes: Optional[int] = MusicFields.number_of_likes