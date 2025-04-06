# from django.test import TestCase

# # Create your tests here.

# from pymongo import MongoClient
# from bson import ObjectId
# from datetime import datetime
# import random

# client = MongoClient("mongodb://localhost:27017/")
# db = client["SPIN_A_YARN_DATABASE"]
# guests = db["guests"]
# messages = db["messages"]
# rooms = db["rooms"]


# room_ids = rooms.find()

# def decorator(func):
#     def _wrapper(*args, **kwargs):
#         print("Before call")
#         print(f"{args}")
#         func(*args, **kwargs)
#         print("After call")
    
#     return _wrapper

# @decorator
# def greetings(content, times):
#     print(f"{content} {times} times")

# greetings("Hello", 5)

# class called:
#     def __init__(self):
#         pass

#     def __call__(self, a):
#         print(a)

# middleware_obj = called()
# middleware_obj(10)