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
        "author_id": author_id,
        "room_id": room_id,
        "content": content,
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
            "participants": [creator_id],
        }
    )

    return str(res.inserted_id)


