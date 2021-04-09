"""REPOSITORIES
Methods to interact with the database
"""

# # Installed # #
import bcrypt
import text2emotion as te
from fastapi.responses import JSONResponse
import wikiquote
from quote2image import generate

# # Package # #
from .models import *
from .exceptions import *
from .database import users, doctors
from .utils import get_time, get_uuid, get_week_timestamp
from .settings import server_settings as settings

# # Native # #
import os
import shutil

__all__ = ("UsersRepository", "DeepFakeRepository", "TherapyRepository", "DoctorRepository")


class UsersRepository:
    @staticmethod
    def get(user_id: str) -> UserRead:
        """Retrieve a single User by its unique id"""
        document = users.find_one({"_id": user_id})
        if not document:
            raise UserNotFoundException(user_id)
        return UserRead(**document)
    
    @staticmethod
    def login(email: str, password: str):
        """Retrieve a single User by its unique id"""
        document = users.find_one({"email": email})
        if not document:
            raise UserNotFoundException(email)
        if bcrypt.hashpw(password.encode('utf-8'), document['password']) != document['password']:
            raise InvalidUserPasswordException(email)
        return {
            "status": True,
            "_id": document["_id"],
            "email": document["email"]
            }

    @staticmethod
    def list() -> UsersRead:
        """Retrieve all the available users"""
        cursor = users.find()
        return [UserRead(**document) for document in cursor]

    @staticmethod
    def create(create: UserCreate) -> UserRead:
        """Create a user and return its Read object"""
        document = create.dict()
        document["created"] = document["updated"] = get_time()
        document["_id"] = get_uuid()
        document["password"] = bcrypt.hashpw(document["password"].encode('utf-8'), bcrypt.gensalt())

        # The time and id could be inserted as a model's Field default factory,
        # but would require having another model for Repository only to implement it

        result = users.insert_one(document)
        assert result.acknowledged

        return UsersRepository.get(result.inserted_id)

    @staticmethod
    def update(user_id: str, update: UserUpdate):
        """Update a user by giving only the fields to update"""
        document = update.dict()
        document["updated"] = get_time()

        result = users.update_one({"_id": user_id}, {"$set": document})
        if not result.modified_count:
            raise UserNotFoundException(identifier=user_id)
    
    @staticmethod
    def update_emotion(id: str, emotion: str, device: bool = False):
        """Update a user's emotion"""
        updated = get_time()
        user_id = id
        if device:
            user_id = users.find_one({"device_id": id})['_id']

        result = users.update_one({"_id": user_id}, {"$push": {
            "states" : {
                "emotion" :emotion.lower(),
                "captured": updated
            }
        }})
        result = users.update_one({"_id": user_id}, {"$set": {
            "current_emotion" : emotion.lower(),
            "updated": updated
        }})

        if not result.modified_count:
            raise UserNotFoundException(identifier=user_id)
        
        return UsersRepository.get(user_id)
    
    @staticmethod
    def emotion_analysis(user_id: str):
        """User's Emotion Analysis"""
        
        document = users.find_one({"_id": user_id})
        emotions = document['states'][::-1]

        start,end  = get_week_timestamp()

        emotion_map = {}
        for emotion in emotions:
            if start <= emotion['captured'] <= end:
                if emotion['emotion'] in emotion_map:
                    emotion_map[emotion['emotion']] += 1
                else:
                    emotion_map[emotion['emotion']] = 1
            else:
                break    
        quote = '7'*81
        while len(quote) > 80:
            title = wikiquote.random_titles(max_titles=1)[0]
            quote = wikiquote.quotes(title, max_quotes=1)[0]
        #print(help(generate))
        img = generate.main(quote + '\n' + title)
        
        folder_path = 'Uploads/' + user_id + '/'
        if not os.path.isdir(folder_path):
            os.mkdir(folder_path)
        
        img.save(folder_path + 'quote.jpg')
        return JSONResponse(
                content={
                    'emotion' : emotion_map,
                    'message' : settings.ftp_server + user_id + '/quote.jpg'
                },
                status_code=200
            )
    
    @staticmethod
    def add_note(user_id: str, note: Note):
        """Update a user's note"""
        note = note.dict()
        updated = get_time()
        
        result = users.update_one({"_id": user_id}, {"$push": {
            "notes" : {
                "note" :note['note'],
                "captured": note['captured'],
                "color": note['color'],
            }
        }})

        emotion = te.get_emotion(note['note'])
        avg_emotion = sum(emotion.values()) / len(emotion)
        for i in emotion:
            if emotion[i] >= avg_emotion:
                UsersRepository.update_emotion(user_id, i.lower())

        if not result.modified_count:
            raise UserNotFoundException(identifier=user_id)
        
        return UsersRepository.get(user_id)
        

    @staticmethod
    def delete(user_id: str):
        """Delete a user given its unique id"""
        result = users.delete_one({"_id": user_id})
        if not result.deleted_count:
            raise UserNotFoundException(identifier=user_id)

    @staticmethod
    def add_profile_pic(picture, user_id):
        """Profile Picture uploaded by user"""
        path = "Uploads/"
        document = users.find_one({"_id": user_id})
        if not document:
            raise UserNotFoundException(user_id)
        
        name = document['name']
        extension = picture.filename.split('.')[-1]

        filename = name + '.' + extension
        folder_path = path + user_id + "/"
        if not os.path.isdir(folder_path):
            os.mkdir(folder_path)

        with open(folder_path + filename, "wb") as buffer:
            shutil.copyfileobj(picture.file, buffer)

        updated = get_time()
        profile_pic = settings.ftp_server + user_id + "/" + filename
        result = users.update_one({"_id": user_id}, {"$set": {
            "profile_pic": profile_pic,
            'updated': updated
            }
        })
        
        return UsersRepository.get(user_id)
        
class DeepFakeRepository:

    @staticmethod
    def add_deepfake_pic(picture, picture_name, user_id):
        """Picture uploaded by user for deepfake"""
        path = "Uploads/"
        document = users.find_one({"_id": user_id})
        if not document:
            raise UserNotFoundException(user_id)
        
        name = document['name']
        extension = picture.filename.split('.')[-1]

        filename = picture_name + '.' + extension
        folder_path = path + user_id + "/deepfake/"
        if not os.path.isdir(folder_path):
            os.mkdir(folder_path)
        
        updated = get_time()
        image = settings.ftp_server + user_id  + "/deepfake/" + filename
        
        result = users.update_one({"_id": user_id}, {"$set": {
            "deepfake": {
                'image' : image,
                'name': filename
            },
            'updated': updated
            }
        })
        
        with open(folder_path + filename, "wb") as buffer:
            shutil.copyfileobj(picture.file, buffer)

        return UsersRepository.get(user_id)
    
    @staticmethod
    def add_deepfake_audio(audio, user_id):
        """Audio uploaded by user for deepfake"""
        path = "Uploads/"
        document = users.find_one({"_id": user_id})
        if not document:
            raise UserNotFoundException(user_id)
        
        name = document['name']
        extension = audio.filename.split('.')[-1]

        deepfake_name = document['deepfake']['name'].split('.')[0]
        filename = deepfake_name + '.' + extension
        folder_path = path + user_id + "/deepfake/"
        if not os.path.isdir(folder_path):
            os.mkdir(folder_path)

        with open(folder_path + filename, "wb") as buffer:
            shutil.copyfileobj(audio.file, buffer)

        updated = get_time()
        audio = settings.ftp_server + user_id + "/deepfake/" + filename
        
        result = users.update_one({"_id": user_id}, {"$set": {
            "deepfake.voice": audio,
            'updated': updated
            }
        })
        
        return UsersRepository.get(user_id)
    
    @staticmethod
    def deepfake(user_id):
        """Files uploaded by admin"""
        path = "Uploads/"
        document = users.find_one({"_id": user_id})
        if not document:
            raise UserNotFoundException(user_id)
        
        name = document['name']
        folder_path = path + user_id + "/deepfake/"

        #deepfake()
        return UsersRepository.get(user_id)

class TherapyRepository:

    @staticmethod
    def music_recommendation(user_id, emotion):
        """Music Recommendation Engine through Emotion"""
        document = users.find_one({"_id": user_id})
        if not document:
            raise UserNotFoundException(user_id)
    
    @staticmethod
    def inspiration_therapy(user_id: str):
        """User's Emotion Analysis"""
        
        document = users.find_one({"_id": user_id})
        
        quotes = []
        for i in range(5):
            quote = '7'*81
            while len(quote) > 80:
                try:
                    title = wikiquote.random_titles(max_titles=1)[0]
                    quote = wikiquote.quotes(title, max_quotes=1)[0]
                except:
                    quote = '7'*81
                    
            img = generate.main(quote + '\n' + title)
            folder_path = 'Uploads/' + user_id + '/'
            if not os.path.isdir(folder_path):
                os.mkdir(folder_path)

            img.save(folder_path + 'quote' + str(i) + '.jpg')
            quotes.append(settings.ftp_server + user_id + '/quote' + str(i) + '.jpg')

        return JSONResponse(
                content={
                    'quotes' : quotes
                },
                status_code=200
            )
        
class DoctorRepository:
    @staticmethod
    def get(doctor_id: str) -> DoctorRead:
        """Retrieve a single Doctor by its unique id"""
        document = doctors.find_one({"_id": doctor_id})
        if not document:
            raise DoctorNotFoundException(doctor_id)
        return DoctorRead(**document)
    
    @staticmethod
    def list() -> DoctorsRead:
        """Retrieve all the available doctors"""
        cursor = doctors.find()
        return [DoctorRead(**document) for document in cursor]

    @staticmethod
    def create(create: DoctorCreate) -> DoctorRead:
        """Create a doctor and return its Read object"""
        document = create.dict()
        document["created"] = document["updated"] = get_time()
        document["_id"] = get_uuid()
        
        # The time and id could be inserted as a model's Field default factory,
        # but would require having another model for Repository only to implement it

        result = doctors.insert_one(document)
        assert result.acknowledged

        return DoctorRepository.get(result.inserted_id)

    @staticmethod
    def update(doctor_id: str, update: DoctorUpdate):
        """Update a doctor by giving only the fields to update"""
        document = update.dict()
        document["updated"] = get_time()

        result = doctors.update_one({"_id": doctor_id}, {"$set": document})
        if not result.modified_count:
            raise DoctorNotFoundException(identifier=doctor_id)        

    @staticmethod
    def delete(doctor_id: str):
        """Delete a doctor given its unique id"""
        result = doctors.delete_one({"_id": doctor_id})
        if not result.deleted_count:
            raise DoctorNotFoundException(identifier=doctor_id)

    @staticmethod
    def add_profile_pic(picture, doctor_id):
        """Profile Picture uploaded by doctor"""
        path = "Uploads/"
        document = doctors.find_one({"_id": doctor_id})
        if not document:
            raise DoctorNotFoundException(doctor_id)
        
        name = document['name']
        extension = picture.filename.split('.')[-1]

        filename = name + '.' + extension
        folder_path = path + doctor_id + "/"
        if not os.path.isdir(folder_path):
            os.mkdir(folder_path)

        with open(folder_path + filename, "wb") as buffer:
            shutil.copyfileobj(picture.file, buffer)

        updated = get_time()
        profile_pic = settings.ftp_server + doctor_id + "/" + filename
        result = doctors.update_one({"_id": doctor_id}, {"$set": {
            "profile_pic": profile_pic,
            'updated': updated
            }
        })
        
        return DoctorRepository.get(doctor_id)
