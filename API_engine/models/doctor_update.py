"""MODELS - DOCTOR - UPDATE
Doctor Update model. All attributes are set as Optional, as we use the PATCH method for update
(in which only the attributes to change are sent on request body)
"""

# # Native # #
from datetime import date
from typing import Optional, List
from contextlib import suppress

# # Package # #
from .common import BaseModel
from .fields import DoctorFields

__all__ = ("DoctorUpdate",)


class DoctorUpdate(BaseModel):
    """Body of Doctor PATCH requests"""
    name: Optional[str] = DoctorFields.name
    gender: Optional[str] = DoctorFields.gender
    mobile: Optional[int] = DoctorFields.mobile
    degree: Optional[str] = DoctorFields.degree
    consultation_place: Optional[str] = DoctorFields.consultation_place
    about_doctor: Optional[str] = DoctorFields.about_doctor
    services_provided: Optional[str] = DoctorFields.services_provided
    address: Optional[str] = DoctorFields.address
    latitude: Optional[float] = DoctorFields.latitude
    longitude: Optional[float] = DoctorFields.longitude
    ratings: Optional[float] = DoctorFields.ratings
    profile_pic: Optional[str] = DoctorFields.profile_pic
    