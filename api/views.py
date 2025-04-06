from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from . import mongo
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .jwt_auth import jwt_required, generate_jwt

# Create your views here.

@csrf_exempt
def join_room_view(request):
    """
    POST DATA FORMAT
    {
        guestName: <str>
        roomId: <id>
    }

    RESPONSE JSON FORMAT
    {
        token: <token>,
    }
    """
    if request.method == "POST":
        data = json.loads(request.body)
        guest_name = data["guestName"]
        room_id = data["roomId"]
        try:
            guest_id = mongo.insert_guest(guest_name)
            mongo.add_participant(guest_id, room_id)
            token = generate_jwt({"guest_id": guest_id, "guest_name": guest_name, "room_id": room_id})
            return JsonResponse({"token": token, "guest_id": guest_id}, status=200)
        except:
            return HttpResponse("Internal Server Error", status=500)


    return JsonResponse({"Response": "OK"}, status=200)

@csrf_exempt
def create_room_view(request):
    """
    POST DATA FORMAT
    {
        guestName: <guest_name>
    }

    RESPONSE JSON FORMAT 
    {
        token: <token>,
        roomId: <id>
    }
    """
    if request.method == "POST":
        data = json.loads(request.body)
        owner_name = data["guestName"]
        
        try:
            guest_id = mongo.insert_guest(owner_name)
            room_id = mongo.insert_room(guest_id)
        except:
            return JsonResponse({"error": "Internal Server Error"}, status=500)

        token = generate_jwt({"guest_id": guest_id, "room_id": room_id})
        return JsonResponse({"token": token, "guest_id": guest_id, "roomId": room_id})
    
    return HttpResponse("Only POST requests are allowed.", status=403)

def get_random_room_view(request):
    """
    RESPONSE JSON FORMAT
    {
        roomId: <id>
    }
    """
    try:
        random_room_id = mongo.get_random_room()
        if random_room_id is None:
            return HttpResponse("No rooms available. Please create your own room or come back later.", status=200)
    except:
        return HttpResponse("Internal Server Error", status=500)
    return JsonResponse({"roomId": random_room_id}, status=200)

@jwt_required
def get_all_messages_view(request):
    """
    RESPONSE JSON FORMAT
    {
       messages: [{author_id: <id>, content: <str>, created: <time>}, ...]
    }
    """
    
    try:
        message_list = mongo.get_all_messages(request.room_id)
        return JsonResponse({"messages": message_list}, status=200)
    except:
        return JsonResponse({"error": "Internal Sever Error"}, status=500)

@jwt_required
def get_room_participants(request):
    """
    RESPONSE JSON FORMAT
    {
        participants: [{guest_id: <id>, guest_name: <str>}, ...]
    }
    """
    try:
        participants = mongo.get_room_participants(request.room_id)
        return JsonResponse({"participants": participants}, status=200)
    except:
        return JsonResponse({"error": "Internal Sever Error"}, status=500)

@jwt_required
def get_current_writer(request):
    """
    RESPONSE JSON FORMAT
    {
        "currentWriterId": <id>,
        "currentWriterName": <str>
    }
    """
    try:
        current_writer_id, current_writer_name = mongo.get_current_writer(request.room_id)
    except:
        return JsonResponse({"error": "Internal Sever Error"}, status=500)
    return  JsonResponse({"currentWriterId": current_writer_id, "currentWriterName": current_writer_name}, status=200)

@csrf_exempt
@jwt_required
def submit_message_view(request):
    """
    POST DATA FORMAT 
    {
        content: <str>
    }
    
    RESPONSE JSON FORMAT
    {
        response: OK
    }

    CHANNEL DATA FORMAT
    {
        event: submit
        authorId: <id>
        content: <str>
    }
    """
    if request.method=="POST":
        data = json.loads(request.body)
        room_id = request.room_id
        guest_id = request.guest_id
        content = data["content"]
   
        try:
            res = mongo.insert_message(guest_id, room_id, content)
        except:
            return JsonResponse({"error": "Internal Server Error"}, status=500)

        #update current writer
        try:
            updated_writer_id = mongo.update_current_writer(room_id)
        except:
            return JsonResponse({"error": "Failed to update current writer"}, status=500)

        if res is not None:
            # Message is added to the database now I want this to communicate to all members of the room
            channel_layer = get_channel_layer()
            event_data = {
                "type": "transmit", 
                "event": "submit",
                "authorId": guest_id,
                "content": content
            }

            async_to_sync(channel_layer.group_send)(
                room_id, event_data
            )

            return JsonResponse({"Response": "OK"}, status=200)
        else:
            return JsonResponse({"error": "Internal Server Error"}, status=500)
            

    return HttpResponse("Only POST requests are allowed", status=403)

