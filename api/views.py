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
        guestId: <guest_id>
        roomId: <room_id>
    }
    """
    if request.method == "POST":
        creator_name = request.POST.get("guestName")
        
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

def submit_message_view(request):
    pass

