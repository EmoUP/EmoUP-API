"""MODELS - DOCTOR - READ
Doctor Read model. Inherits from DoctorCreate and adds the doctor_id field, which is the _id field on Mongo documents
"""

# # Native # #
from datetime import datetime
from typing import Optional, List

# # Installed # #
import pydantic
from dateutil.relativedelta import relativedelta

# # Package # #
from .doctor_create import DoctorCreate
from .fields import DoctorFields

__all__ = ("DoctorRead", "DoctorsRead")


class DoctorRead(DoctorCreate):
    """Body of Doctor GET and POST responses"""
    doctor_id: str = DoctorFields.doctor_id
    created: int = DoctorFields.created
    updated: int = DoctorFields.updated

    @pydantic.root_validator(pre=True)
    def _set_doctor_id(cls, data):
        """Swap the field _id to doctor_id (this could be done with field alias, by setting the field as "_id"
        and the alias as "doctor_id", but can be quite confusing)"""
        document_id = data.get("_id")
        if document_id:
            data["doctor_id"] = document_id
        return data

    class Config(DoctorCreate.Config):
        extra = pydantic.Extra.ignore  # if a read document has extra fields, ignore them


DoctorsRead = List[DoctorRead]
