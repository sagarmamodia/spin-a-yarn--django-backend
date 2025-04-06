import json
import os
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .jwt_auth import decode_jwt
from . import mongo

class RoomConsumer(WebsocketConsumer):
    def connect(self):
        token = self.scope['url_route']['kwargs']['token']
        try:
            payload = decode_jwt(token)
            self.guest_id = payload['guest_id']
            self.room_id = payload['room_id']
        except:
            return

        async_to_sync(self.channel_layer.group_add)(
            self.room_id, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        mongo.update_db(self.guest_id, self.room_id)
        
        async_to_sync(self.channel_layer.group_discard)(
            self.room_id, self.channel_name
        ) 
    
    def receive(self, text_data):
        """
        MESSAGE FORMAT 
        {
            event: submit
            authorId: <id>
            content: <str>
        }

        {
            event: live
            authorId: <id>
            content: <str>
        }
        """

        data_parsed = json.loads(text_data)
        event_data = {"type": "transmit", 
                        "event": data_parsed["event"], 
                        "authorId": data_parsed["authorId"], 
                        "content": data_parsed["content"] 
                    }
        
        async_to_sync(self.channel_layer.group_send)(
            self.room_id, event_data
        )
    
    def transmit(self, event):
        event_dict = {"event": event["event"], "authorId": event["authorId"], "content": event["content"]}
        self.send(text_data=json.dumps(event_dict))
