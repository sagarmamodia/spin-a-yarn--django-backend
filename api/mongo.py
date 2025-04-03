from pymongo import MongoClient
from django.conf import settings
from bson import ObjectId
from datetime import datetime

client = MongoClient(settings.MONGO_URI)
db = client[settings.MONGO_DB_NAME]
guests = db["guests"]
messages = db["messages"]
rooms = db["rooms"]

def insert_message(author_id, room_id, content):
    message = {
        "author_id": ObjectId(author_id),
        "room_id": ObjectId(room_id),
        "content": ObjectId(content),
        "created": datetime.now(tz=datetime.timezone.utc),
    }

    res = messages.insert_one(message)
    return str(res.inserted_id)

def insert_guest(guest_name):
    res = guests.insert_one({"name": guest_name})
    return str(res.inserted_id)

def insert_room(creator_id):
    """
    creator -> guest_id
    """
    res = rooms.insert_one(
        {
            "creator_id": ObjectId(creator_id),
            "participants": [ObjectId(creator_id)],
        }
    )

    return str(res.inserted_id)

def get_guest(guest_id):
    res = guests.find_one({"_id": ObjectId(guest_id)})
    return res

def get_room(room_id):
    res = rooms.find_one({"_id": ObjectId(room_id)})
    return res

def submit_message(author_id, room_id, content):
    res = messages.insert_one({
        "author_id": ObjectId(author_id),
        "room_id": ObjectId(room_id),
        "content": content,
    })

    return str(res.inserted_id)

