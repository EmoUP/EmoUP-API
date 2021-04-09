"""SETTINGS
Settings loaders using Pydantic BaseSettings classes (load from environment variables / dotenv file)
"""

# # Installed # #
import pydantic

__all__ = ("api_settings", "server_settings", "mongo_settings")


class BaseSettings(pydantic.BaseSettings):
    class Config:
        env_file = ".env"


class APISettings(BaseSettings):
    title: str = "Emoup API"
    host: str = "0.0.0.0"
    port: int = 5000
    log_level: str = "INFO"

    class Config(BaseSettings.Config):
        env_prefix = "API_"

class ServerSettings(BaseSettings):
    ftp_server : str = 'http://52.188.203.118:5003/'
    class Config(BaseSettings.Config):
        env_prefix = "Server_"

class MongoSettings(BaseSettings):
    uri: str = "mongodb://52.188.203.118:5001"
    user: str = 'emoup'
    password: str = '4Fjr#3H*O&2vf2'
    database: str = "emoup"
    users: str = "users"

    class Config(BaseSettings.Config):
        env_prefix = "MONGO_"


api_settings = APISettings()
server_settings = ServerSettings()
mongo_settings = MongoSettings()
