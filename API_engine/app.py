"""APP
FastAPI app definition, initialization and definition of routes
"""

# # Installed # #
import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi import status as statuscode

# # Package # #
from .models import *
from .exceptions import *
from .repositories import UsersRepository, DeepFakeRepository, TherapyRepository, DoctorRepository, MusicRepository
from .middlewares import request_handler
from .settings import api_settings as settings

__all__ = ("app", "run")


app = FastAPI(
    title=settings.title
)
app.middleware("http")(request_handler)


@app.get(
    "/users",
    response_model=UsersRead,
    description="List all the available users",
    tags=["Users"]
)
def _list_users():
    # TODO Filters
    return UsersRepository.list()


@app.get(
    "/users/{user_id}",
    response_model=UserRead,
    description="Get a single user by its unique ID",
    responses=get_exception_responses(UserNotFoundException),
    tags=["Users"]
)
def _get_user(user_id: str):
    return UsersRepository.get(user_id)


@app.post(
    "/users",
    description="Create a new user",
    response_model=UserRead,
    status_code=statuscode.HTTP_201_CREATED,
    responses=get_exception_responses(UserAlreadyExistsException),
    tags=["Users"]
)
def _create_user(create: UserCreate):
    return UsersRepository.create(create)

@app.post(
    "/users/login",
    description="Login into system",
    responses=get_exception_responses(UserNotFoundException),
    tags=["Users"]
)
def _login_user(email: str, password: str):
    return UsersRepository.login(email,password)

@app.patch(
    "/users/{user_id}",
    description="Update a single user by its unique ID, providing the fields to update",
    status_code=statuscode.HTTP_204_NO_CONTENT,
    responses=get_exception_responses(UserNotFoundException, UserAlreadyExistsException),
    tags=["Users"]
)
def _update_user(user_id: str, update: UserUpdate):
    UsersRepository.update(user_id, update)


@app.delete(
    "/users/{user_id}",
    description="Delete a single user by its unique ID",
    status_code=statuscode.HTTP_204_NO_CONTENT,
    responses=get_exception_responses(UserNotFoundException),
    tags=["Users"]
)
def _delete_user(user_id: str):
    UsersRepository.delete(user_id)

@app.post(
    "/users/add-profile-pic",
    response_model=UserRead,
    description="Add Profile Pic",
    tags=["Users"]
)
def _add_profile_pic(user_id: str, picture: UploadFile = File(...)):
    return UsersRepository.add_profile_pic(picture, user_id)

@app.post(
    "/users/update-emotion",
    response_model=UserRead,
    description="Update current Emotion of User",
    tags=["Users"]
)
def _update_emotion(user_id: str, emotion: str, device: str):
    return UsersRepository.update_emotion(user_id, emotion, True if device == "true" else False)

@app.get(
    "/users/emotion-analysis/{user_id}",
    description="Get Emotion Analysis of User",
    tags=["Users"]
)
def _emotion_analysis(user_id: str):
    return UsersRepository.emotion_analysis(user_id)

@app.post(
    "/users/add-note",
    response_model=UserRead,
    description="Add Note of User",
    tags=["Users"]
)
def _add_note(user_id: str, note: Note):
    return UsersRepository.add_note(user_id, note)
  
@app.post(
    "/deep-fake/picture",
    description="Add DeepFake Pic",
    tags=["Deep Fake"]
)
def _add_deepfake_pic(user_id: str, name: str, picture: UploadFile = File(...)):
    return DeepFakeRepository.add_deepfake_pic(picture, name, user_id)

@app.post(
    "/deep-fake/audio",
    description="Add DeepFake Audio",
    tags=["Deep Fake"]
)
def _add_deepfake_audio(user_id: str, audio: UploadFile = File(...)):
    return DeepFakeRepository.add_deepfake_audio(audio, user_id)

@app.get(
    "/deep-fake/result/{user_id}",
    response_model=UsersRead,
    description="Add DeepFake",
    tags=["Deep Fake"]
)
def _deepfake(user_id: str):
    return DeepFakeRepository.deepfake(user_id)

@app.get(
    "/therapies/music-recommendation/{user_id}",
    description="Give Music recommendations based on emotions",
    tags=["Therapies"]
)
def _music_recommendation(user_id: str):
    return TherapyRepository.music_recommendation(user_id)

@app.get(
    "/therapies/inspiration/{user_id}",
    description="Give Inspiration quotes",
    tags=["Therapies"]
)
def _inspiration_therapy(user_id: str):
    return TherapyRepository.inspiration_therapy(user_id)

@app.get(
    "/doctors",
    response_model=DoctorsRead,
    description="List all the available doctors",
    tags=["Doctors"]
)
def _list_doctors():
    # TODO Filters
    return DoctorRepository.list()


@app.get(
    "/doctors/{doctor_id}",
    response_model=DoctorRead,
    description="Get a single doctor by its unique ID",
    responses=get_exception_responses(DoctorNotFoundException),
    tags=["Doctors"]
)
def _get_doctor(doctor_id: str):
    return DoctorRepository.get(doctor_id)


@app.post(
    "/doctors",
    description="Create a new doctor",
    response_model=DoctorRead,
    status_code=statuscode.HTTP_201_CREATED,
    responses=get_exception_responses(DoctorAlreadyExistsException),
    tags=["Doctors"]
)
def _create_doctor(create: DoctorCreate):
    return DoctorRepository.create(create)

@app.patch(
    "/doctors/{doctor_id}",
    description="Update a single doctor by its unique ID, providing the fields to update",
    status_code=statuscode.HTTP_204_NO_CONTENT,
    responses=get_exception_responses(DoctorNotFoundException, DoctorAlreadyExistsException),
    tags=["Doctors"]
)
def _update_doctor(doctor_id: str, update: DoctorUpdate):
    DoctorRepository.update(doctor_id, update)


@app.delete(
    "/doctors/{doctor_id}",
    description="Delete a single doctor by its unique ID",
    status_code=statuscode.HTTP_204_NO_CONTENT,
    responses=get_exception_responses(DoctorNotFoundException),
    tags=["Doctors"]
)
def _delete_doctor(doctor_id: str):
    DoctorRepository.delete(doctor_id)

@app.post(
    "/doctors/add-profile-pic",
    response_model=DoctorRead,
    description="Add Profile Pic",
    tags=["Doctors"]
)
def _add_profile_pic(doctor_id: str, picture: UploadFile = File(...)):
    return DoctorRepository.add_profile_pic(picture, doctor_id)

@app.get(
    "/musics",
    response_model=MusicsRead,
    description="List all the available musics",
    tags=["Musics"]
)
def _list_musics():
    # TODO Filters
    return MusicRepository.list()


@app.get(
    "/musics/{music_id}",
    response_model=MusicRead,
    description="Get a single music by its unique ID",
    responses=get_exception_responses(MusicNotFoundException),
    tags=["Musics"]
)
def _get_music(music_id: str):
    return MusicRepository.get(music_id)


@app.post(
    "/musics",
    description="Create a new music",
    response_model=MusicRead,
    status_code=statuscode.HTTP_201_CREATED,
    responses=get_exception_responses(MusicAlreadyExistsException),
    tags=["Musics"]
)
def _create_music(create: MusicCreate):
    return MusicRepository.create(create)

@app.patch(
    "/musics/{music_id}",
    description="Update a single music by its unique ID, providing the fields to update",
    status_code=statuscode.HTTP_204_NO_CONTENT,
    responses=get_exception_responses(MusicNotFoundException, MusicAlreadyExistsException),
    tags=["Musics"]
)
def _update_music(music_id: str, update: MusicUpdate):
    MusicRepository.update(music_id, update)


@app.delete(
    "/musics/{music_id}",
    description="Delete a single music by its unique ID",
    status_code=statuscode.HTTP_204_NO_CONTENT,
    responses=get_exception_responses(MusicNotFoundException),
    tags=["Musics"]
)
def _delete_music(music_id: str):
    MusicRepository.delete(music_id)

def run():
    """Run the API using Uvicorn"""
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        log_level=settings.log_level.lower()
    )
