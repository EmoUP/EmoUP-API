"""MODELS - DOCTOR
The Doctor model
"""

# # Package # #
from .common import BaseModel
from .fields import DoctorFields
from .doctor_update import DoctorUpdate

__all__ = ("DoctorCreate",)


class DoctorCreate(DoctorUpdate):
    """The information of a Doctor"""
    name: str = DoctorFields.name
    gender: str = DoctorFields.gender
    mobile: int = DoctorFields.mobile
    degree: str = DoctorFields.degree
    consultation_place: str = DoctorFields.consultation_place
    about_doctor: str = DoctorFields.about_doctor
    services_provided: str = DoctorFields.services_provided
    address: str = DoctorFields.address
    latitude: float = DoctorFields.latitude
    longitude: float = DoctorFields.longitude
    ratings: float = DoctorFields.ratings