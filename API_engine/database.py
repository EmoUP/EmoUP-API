"""DATABASE
MongoDB database initialization
"""

# # Installed # #
from pymongo import MongoClient
from pymongo.collection import Collection

# # Package # #
from .settings import mongo_settings as settings

__all__ = ("client", "collection")

client = MongoClient(settings.uri)
client.admin.authenticate(settings.user, settings.password, mechanism = 'SCRAM-SHA-1', source='admin')
users: Collection = client[settings.database][settings.users]
doctors: Collection = client[settings.database][settings.doctors]
musics: Collection = client[settings.database][settings.musics]
