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
from .repositories import UsersRepository, DeepFakeRepository
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
    tags=["users"]
)
def _list_users():
    # TODO Filters
    return UsersRepository.list()


@app.get(
    "/users/{user_id}",
    response_model=UserRead,
    description="Get a single user by its unique ID",
    responses=get_exception_responses(UserNotFoundException),
    tags=["users"]
)
def _get_user(user_id: str):
    return UsersRepository.get(user_id)


@app.post(
    "/users",
    description="Create a new user",
    response_model=UserRead,
    status_code=statuscode.HTTP_201_CREATED,
    responses=get_exception_responses(UserAlreadyExistsException),
    tags=["users"]
)
def _create_user(create: UserCreate):
    return UsersRepository.create(create)

@app.post(
    "/users/login",
    description="Login into system",
    responses=get_exception_responses(UserNotFoundException),
    tags=["users"]
)
def _login_user(email: str, password: str):
    return UsersRepository.login(email,password)

@app.patch(
    "/users/{user_id}",
    description="Update a single user by its unique ID, providing the fields to update",
    status_code=statuscode.HTTP_204_NO_CONTENT,
    responses=get_exception_responses(UserNotFoundException, UserAlreadyExistsException),
    tags=["users"]
)
def _update_user(user_id: str, update: UserUpdate):
    UsersRepository.update(user_id, update)


@app.delete(
    "/users/{user_id}",
    description="Delete a single user by its unique ID",
    status_code=statuscode.HTTP_204_NO_CONTENT,
    responses=get_exception_responses(UserNotFoundException),
    tags=["users"]
)
def _delete_user(user_id: str):
    UsersRepository.delete(user_id)

@app.post(
    "/users/add-profile-pic",
    response_model=UserRead,
    description="Add Profile Pic",
    tags=["users"]
)
def _add_profile_pic(user_id: str, picture: UploadFile = File(...)):
    return UsersRepository.add_profile_pic(picture, user_id)

@app.post(
    "/users/update-emotion",
    response_model=UserRead,
    description="Update current Emotion of User",
    tags=["users"]
)
def _update_emotion(user_id: str, emotion: str):
    return UsersRepository.update_emotion(user_id, emotion)
  
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

def run():
    """Run the API using Uvicorn"""
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        log_level=settings.log_level.lower()
    )
