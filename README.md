# EmoUP AI API

The code is intended to create the whole OpenAPI documentation with the maximum detail, including full, detailed models for requests, responses and errors.
- OPEN API http://52.188.203.118:5000/docs
- REDOC http://52.188.203.118:5000/redoc

## Endpoints

Endpoints define the whole CRUD operations that can be performed on User entities:

- GET `/docs` - OpenAPI documentation (generated by FastAPI)
- GET `/users` - list all available users
- GET `/users/{user_id}` - get a single user by its unique ID
- POST `/users` - create a new user
- PATCH `/users/{user_id}` - update an existing user
- DELETE `/users/{user_id}` - delete an existing user

## Project structure (modules)

- `app.py`: initialization of FastAPI and all the routes used by the API. On APIs with more endpoints and different entities, would be better to split the routes in different modules by their context or entity.
- `models`: definition of all model classes. As we are using MongoDB, we can use the same JSON schema for API request/response and storage. However, different classes for the same entity are required, depending on the context:
    - `doctor_update.py`: model used as PATCH request body. Includes all the fields that can be updated, set as optional.
    - `doctor_create.py`: model used as POST request body. Includes all the fields from the Update model, but all those fields that are required on Create, must be re-declared (in type and Field value).
    - `doctor_read.py`: model used as GET and POST response body. Includes all the fields from the Create model, plus the doctor_id (which comes from the _id field in Mongo document) and the age (calculated from the date of birth, if any).
    - `music_update.py`: model used as PATCH request body. Includes all the fields that can be updated, set as optional.
    - `music_create.py`: model used as POST request body. Includes all the fields from the Update model, but all those fields that are required on Create, must be re-declared (in type and Field value).
    - `music_read.py`: model used as GET and POST response body. Includes all the fields from the Create model, plus the music_id (which comes from the _id field in Mongo document) and the age (calculated from the date of birth, if any).
    - `user_update.py`: model used as PATCH request body. Includes all the fields that can be updated, set as optional.
    - `user_create.py`: model used as POST request body. Includes all the fields from the Update model, but all those fields that are required on Create, must be re-declared (in type and Field value).
    - `user_read.py`: model used as GET and POST response body. Includes all the fields from the Create model, plus the user_id (which comes from the _id field in Mongo document) and the age (calculated from the date of birth, if any).
    - `user_address.py`: part of the User model, address attribute.
    - `user_notes.py`: part of the User model, notes attribute.
    - `user_emotion.py`: part of the User model, emotion attribute.
    - `common.py`: definition of the common BaseModel, from which all the model classes inherit, directly or indirectly.
    - `fields.py`: definition of Fields, which are the values of the models attributes. Their main purpose is to complete the OpenAPI documentation by providing a description and examples. Fields are declared outside the classes because of the re-declaration required between Update and Create models.
    - `errors.py`: error models. They are referenced on Exception classes defined in `exceptions.py`.
- `database.py`: initialization of MongoDB client. Actually is very short as Mongo/pymongo do not require to pre-connecting to Mongo or setup the database/collection, but with other databases (like SQL-like using SQLAlchemy) this can get more complex.
- `exceptions.py`: custom exceptions, that can be translated to JSON responses the API can return to clients (mainly if a User does not exist or already exists).
- `middlewares.py`: the Request Handler middleware catches the exceptions raised while processing requests, and tries to translate them into responses given to the clients.
- `repositories.py`: methods that interact with the Mongo database to read or write User data. These methods are directly called from the route handlers.
- `exceptions.py`: custom exceptions raised during request processing. They have an error model associated, so OpenAPI documentation can show the error models. Also define the error message and status code returned.
- `settings.py`: load of application settings through environment variables or dotenv file, using Pydantic's BaseSettings classes.
- `utils.py`: misc helper functions.
- `tests`: acceptance+integration tests, that run directly against the API endpoints and real Mongo database.

## Requirements

- Python >= 3.7
- Requirements listed on [requirements.txt](requirements.txt)
- Running MongoDB server
