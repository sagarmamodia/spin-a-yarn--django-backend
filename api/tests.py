# from django.test import TestCase

# # Create your tests here.

from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
import random

client = MongoClient("mongodb://localhost:27017/")
db = client["SPIN_A_YARN_DATABASE"]
guests = db["guests"]
messages = db["messages"]
rooms = db["rooms"]


room_ids = rooms.find()


