"""MODELS - FIELDS
Definition of Fields used on model classes attributes.
We define them separately because the UserUpdate and UserCreate models need to re-define their attributes,
as they change from Optional to required.
Address could define its fields on the model itself, but we define them here for convenience
"""

# # Installed # #
from pydantic import Field

# # Package # #
from ..utils import get_time, get_uuid

__all__ = ("UserFields", "AddressFields")

_string = dict(min_length=1)
"""Common attributes for all String fields"""
_unix_ts = dict(example=get_time())
"""Common attributes for all Unix timestamp fields"""


class UserFields:
    name = Field(
        description="Full name of this user",
        example="John Doe",
        **_string
    )
    email = Field(
        description="Email of this user",
        example="johndoe@gmail.com",
        **_string
    )
    password = Field(
        description="Password of this user",
        example="**********",
        **_string
    )
    profile_pic = Field(
        description="Profile Photo of this user",
        example="http://emoupup.com/1/profile",
        **_string
    )
    current_emotion = Field(
        description="Current Emotion of this user",
        example="Happy",
        **_string
    )
    address = Field(
        description="Address object where this user live"
    )
    address_update = Field(
        description=f"{address.description}. When updating, the whole Address object is required, as it gets replaced"
    )
    birth = Field(
        description="Date of birth, in format YYYY-MM-DD, or Unix timestamp",
        example="1999-12-31"
    )
    states = Field(
        description="Emotion state of user"
    )
    notes = Field(
        description="Notes of user"
    )
    deepfake = Field(
        description="DeepFake repo of user"
    )
    age = Field(
        description="Age of this user, if date of birth is specified",
        example=20
    )
    device_id = Field(
        description="Emoup Device id of this user in the database",
        example="1BDKfbibi1234"
    )
    user_id = Field(
        description="Unique identifier of this user in the database",
        example=get_uuid(),
        min_length=36,
        max_length=36
    )
    """The user_id is the _id field of Mongo documents, and is set on UsersRepository.create"""

    created = Field(
        alias="created",
        description="When the user was registered (Unix timestamp)",
        **_unix_ts
    )
    """Created is set on UsersRepository.create"""
    updated = Field(
        alias="updated",
        description="When the user was updated for the last time (Unix timestamp)",
        **_unix_ts
    )
    """Created is set on UsersRepository.update (and initially on create)"""


class StateFields:
    emotion = Field(
        description="Emotion of the user",
        example="Happy",
        **_string
    )
    captured = Field(
        description="Capture time of the emotion (Unix timestamp)",
        **_unix_ts
    )
    
class NoteFields:
    note = Field(
        description="Note of the user",
        example="Hello, I finally won, really happy!",
        **_string
    )
    captured = Field(
        description="Capture time of the note",
        example="06/04/2020",
        **_string
    )
    color = Field(
        description="Color selected by the user",
        example="red",
        **_string
    )
    
class DeepFakeFields:
    name = Field(
        description="Name of the person given by user",
        example="Johana Doe",
        **_string
    )
    image = Field(
        description="Image of this person given by user",
        example="http://emoupup.com/1/deepfake/1.jpg",
        **_string
    )
    voice = Field(
        description="Voice of this person given by the user",
        example="http://emoupup.com/1//deepfake/1.wav",
        **_string
    )
    output = Field(
        description="Output Video of this person",
        example="http://emoupup.com/1/deepfake/1.mp4",
        **_string
    )
    
class AddressFields:
    street = Field(
        description="Main address line",
        example="141, Navlakha",
        **_string
    )
    city = Field(
        description="City",
        example="Indore",
        **_string
    )
    state = Field(
        description="State, province and/or region",
        example="Madhya Pradesh",
        **_string
    )
    zip_code = Field(
        description="Postal/ZIP code",
        example="452005",
        **_string
    )

class DoctorFields:
    name = Field(
        description="Full name of this doctor",
        example="John Doe",
        **_string
    )
    gender = Field(
        description="Gender of this doctor",
        example="Male",
        **_string
    )
    mobile = Field(
        description="Mobile of this doctor",
        example=9999988888
    )
    profile_pic = Field(
        description="Profile Photo of this doctor",
        example="http://emoupup.com/1/profile",
        **_string
    )
    degree = Field(
        description="Degree of this doctor",
        example="M.B.B.S",
        **_string
    )
    about_doctor = Field(
        description="About Doctor",
        example="Professional surgeon",
        **_string
    )
    consultation_place = Field(
        description="Consultation Place address of this doctor",
        example="Vijaynagar, Indore",
        **_string
    )
    services_provided = Field(
        description="Services provided by this doctor",
        example="surgeon",
        **_string
    )
    address = Field(
        description="Address of this doctor",
        example="Vijaynagar, Indore",
        **_string
    )
    about_doctor = Field(
        description="About Doctor of this doctor",
        example="Professional surgeon",
        **_string
    )
    latitude = Field(
        description="Latitude of this doctor's location",
        example=22.756
    )
    longitude = Field(
        description="Longitude of this doctor's location",
        example=77.756
    )
    ratings = Field(
        description="Rating of this doctor",
        example=4.5
    )
    doctor_id = Field(
        description="Unique identifier of this doctor in the database",
        example=get_uuid(),
        min_length=36,
        max_length=36
    )
    """The doctor_id is the _id field of Mongo documents, and is set on DoctorsRepository.create"""

    created = Field(
        alias="created",
        description="When the doctor was registered (Unix timestamp)",
        **_unix_ts
    )
    """Created is set on DoctorsRepository.create"""
    updated = Field(
        alias="updated",
        description="When the doctor was updated for the last time (Unix timestamp)",
        **_unix_ts
    )
    """Created is set on DoctorsRepository.update (and initially on create)"""

