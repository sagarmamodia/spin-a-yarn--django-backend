from pymongo import MongoClient
from django.conf import settings
from bson import ObjectId
from datetime import datetime
import random

client = MongoClient(settings.MONGO_URI)
db = client[settings.MONGO_DB_NAME]
guests = db["guests"]
messages = db["messages"]
rooms = db["rooms"]

def insert_message(author_id, room_id, content):
    message = {
        "author_id": ObjectId(author_id),
        "room_id": ObjectId(room_id),
        "content": content,
        "created": datetime.now(),
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
            "current_writer_id": ObjectId(creator_id)
        }
    )

    return str(res.inserted_id)

def add_participant(guest_id, room_id):
    rooms.update_one(
        {"_id": ObjectId(room_id)},
        {"$push": {"participants": ObjectId(guest_id)}}
    )

    return "OK"

def get_random_room():
    room_ids = list(rooms.find())
    if len(room_ids) == 0:
        return None
    
    idx = random.randint(0, len(room_ids)-1)
    room_id = str(room_ids[idx]["_id"])
    return room_id

def get_all_messages(room_id):
    query_result = messages.find({"room_id": ObjectId(room_id)})

    message_list = []
    for message in query_result:
        message_list.append({
            "author_id": str(message["author_id"]),
            "content": message["content"],
            "created": message["created"],
        })

    return message_list

def get_room_participants(room_id):
    room = rooms.find_one({"_id": ObjectId(room_id)})
    participant_ids = room["participants"]

    participants = []
    # participants = guests.find({"_id": {"$in": participant_ids}})
    for _id in participant_ids:
        guest_name = guests.find_one({"_id": _id})["name"]
        participants.append({"guestId": str(_id), "guestName": guest_name})
    
    return participants

def update_current_writer(room_id):
    room = rooms.find_one({"_id": ObjectId(room_id)})
    current_writer_id = room['current_writer_id']
    participants = room["participants"]
    i = 0
    for p_id in participants:
        if p_id == current_writer_id:
            i += 1
            break
        i += 1
    
    if i<len(participants):
        rooms.update_one(
            {"_id": ObjectId(room_id)},
            {"$set": {"current_writer_id": participants[i]}}
        )
        return str(participants[i])
    else:
        rooms.update_one(
            {"_id": ObjectId(room_id)},
            {"$set": {"current_writer_id": participants[0]}}
        )
        return str(participants[0])

def get_current_writer(room_id):
    current_writer_id = rooms.find_one({"_id": ObjectId(room_id)})["current_writer_id"]
    current_writer_name = guests.find_one({"_id": current_writer_id})["name"]
    return str(current_writer_id), current_writer_name

def update_db(guest_id, room_id):
    guests.delete_one({"_id": ObjectId(guest_id)})
    rooms.update_one(
        {"_id": ObjectId(room_id)},
        {"$pull": {"participants": ObjectId(guest_id)}}
        )
    
    partcipants = get_room_participants(room_id)
    if len(partcipants) == 0:
        rooms.delete_one({"_id": ObjectId(room_id)})
        messages.delete_many({"room_id": ObjectId(room_id)})

    return "OK"