from django.urls import re_path
from . import consumers

websocket_patterns = [
    re_path(r"ws/rooms/(?P<room_id>\w+)/$", consumers.RoomConsumer.as_asgi()),
]