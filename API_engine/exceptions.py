"""EXCEPTIONS
Custom exceptions that will make the API return certain HTTP responses to the client.
Each exception has a message, statuscode and response model (from models.errors).
Each exception must be raised using the kwargs (fields) of the associated model.
Exceptions can return the HTTP response model (Response/JSONResponse) and part of the response model definition.
"""

# # Native # #
from typing import Type

# # Installed # #
from fastapi.responses import JSONResponse
from fastapi import status as statuscode

# # Package # #
from .models.errors import *

__all__ = (
    "BaseAPIException", "BaseIdentifiedException",
    "NotFoundException", "AlreadyExistsException",
    "UserNotFoundException", "InvalidUserPasswordException", 
    "UserAlreadyExistsException", "get_exception_responses",
    "DoctorNotFoundException", "DoctorAlreadyExistsException",
)


class BaseAPIException(Exception):
    """Base error for custom API exceptions"""
    message = "Generic error"
    code = statuscode.HTTP_500_INTERNAL_SERVER_ERROR
    model = BaseError

    def __init__(self, **kwargs):
        kwargs.setdefault("message", self.message)
        self.message = kwargs["message"]
        self.data = self.model(**kwargs)

    def __str__(self):
        return self.message

    def response(self):
        return JSONResponse(
            content=self.data.dict(),
            status_code=self.code
        )

    @classmethod
    def response_model(cls):
        return {cls.code: {"model": cls.model}}


class BaseIdentifiedException(BaseAPIException):
    """Base error for exceptions related with entities, uniquely identified"""
    message = "Entity error"
    code = statuscode.HTTP_500_INTERNAL_SERVER_ERROR
    model = BaseIdentifiedError

    def __init__(self, identifier, **kwargs):
        super().__init__(identifier=identifier, **kwargs)


class NotFoundException(BaseIdentifiedException):
    """Base error for exceptions raised because an entity does not exist"""
    message = "The entity does not exist"
    code = statuscode.HTTP_404_NOT_FOUND
    model = NotFoundError


class AlreadyExistsException(BaseIdentifiedException):
    """Base error for exceptions raised because an entity already exists"""
    message = "The entity already exists"
    code = statuscode.HTTP_409_CONFLICT
    model = AlreadyExistsError


class UserNotFoundException(NotFoundException):
    """Error raised when a user does not exist"""
    message = "The user does not exist"

class InvalidUserPasswordException(NotFoundException):
    """Error raised when a user/password is incorrect"""
    message = "The user/password is incorrect"


class UserAlreadyExistsException(AlreadyExistsException):
    """Error raised when a user already exists"""
    message = "The user already exists"

class DoctorNotFoundException(NotFoundException):
    """Error raised when a doctor does not exist"""
    message = "The doctor does not exist"

class DoctorAlreadyExistsException(AlreadyExistsException):
    """Error raised when a doctor already exists"""
    message = "The doctor already exists"


def get_exception_responses(*args: Type[BaseAPIException]) -> dict:
    """Given BaseAPIException classes, return a dict of responses used on FastAPI endpoint definition, with the format:
    {statuscode: schema, statuscode: schema, ...}"""
    responses = dict()
    for cls in args:
        responses.update(cls.response_model())
    return responses
