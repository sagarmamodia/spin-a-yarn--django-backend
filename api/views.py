from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from . import mongo

# Create your views here.

def join_room_view(request):
    pass

@csrf_exempt
def create_room_view(request):
    """
    POST DATA FORMAT
    {
        guestName: <guest_name>
    }

    RESPONSE JSON FORMAT 
    {
        guestId: <id>
        roomId: <id>
    }
    """
    if request.method == "POST":
        data = request.body
        creator_name = data["guestName"]
        
        guest_id = mongo.insert_guest(creator_name)
        room_id = mongo.insert_room(guest_id)

        res_data = {"guest_id": guest_id, "room_id": room_id}   
        
        return JsonResponse(res_data)
    
    return HttpResponse("Only POST requests are allowed.", status=403)

def get_random_room_view(request):
    pass

def get_all_messages_view(request, room_id):
    pass

def get_room_participants(request, room_id):
    pass

def get_current_writer_view(request, room_id):
    pass

def set_current_writer_view(request):
    pass

@csrf_exempt
def submit_message_view(request):
    """
    POST DATA FORMAT 
    {
        roomId: <id>
        guestId: <id>
        content: <str>
    }

    RESPONSE JSON FORMAT
    {
        
    }
    """
    if request.method=="POST":
        data = json.loads(request.body)
        room_id = data["roomId"]
        guest_id = data["guestId"]
        content = data["content"]
        
        # check if both room and guest exists
        if mongo.get_room(room_id) is None or mongo.get_guest(guest_id) is None:
            return HttpResponse("Incorrect roomId or guestId", status=404)

        res = mongo.submit_message(guest_id, room_id, content)
        if res is not None:
            return JsonResponse({"Response": "OK"}, status=200)
        else:
            return HttpResponse("Internal Servor error", status=500)

    return HttpResponse("Only POST requests are allowed", status=403)

