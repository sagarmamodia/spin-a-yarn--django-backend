from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from . import mongo

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
        Response: OK
    }
    """
    if request.method == "POST":
        data = json.loads(request.body)
        guest_name = data["guestName"]
        room_id = data["roomId"]
        try:
            guest_id = mongo.insert_guest(guest_name)
            print(guest_id, room_id)
            mongo.add_participant(guest_id, room_id)
            return JsonResponse({"Response": "OK"}, status=200)
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
        guestId: <id>
        roomId: <id>
    }
    """
    if request.method == "POST":
        data = json.loads(request.body)
        creator_name = data["guestName"]
        
        try:
            guest_id = mongo.insert_guest(creator_name)
            room_id = mongo.insert_room(guest_id)
        except:
            return HttpResponse("Internal Server Error", status=500)

        res_data = {"guest_id": guest_id, "room_id": room_id}   
        
        return JsonResponse(res_data)
    
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
    except:
        return HttpResponse("Internal Server Error", status=500)
    return JsonResponse({"roomId": random_room_id}, status=200)

def get_all_messages_view(request, room_id):
    """
    RESPONSE JSON FORMAT
    {
       messages: [{author_id: <id>, content: <str>, created: <time>}, ...]
    }
    """
    
    try:
        message_list = mongo.get_all_messages(room_id)
        return JsonResponse({"messages": message_list}, status=200)
    except:
        return HttpResponse("Internal Server Error", status=500)

@csrf_exempt
def get_room_participants(request, room_id):
    """
    RESPONSE JSON FORMAT
    {
        participants: [<id>, ...]
    }
    """
    try:
        participants = mongo.get_room_participants(room_id)
        return JsonResponse({"participants": participants}, status=200)
    except:
        return HttpResponse("Internal Sever Error", status=500)

def update_current_writer_view(request):
    """
    POST DATA FORMAT
    {
        "currentWriterId": <id>,
        "roomId": <id>
    }
    
    RESPONSE JSON FORMAT
    {
        "currentWriterId": <id>,
    }
    """
    if request.method == "POST":
        data = json.loads(request.body)
        current_writer_id = data["currentWriterId"]
        room_id = data["room_id"]
        try:
            updated_writer_id = mongo.update_current_writer(current_writer_id, room_id)
            return JsonResponse({"currentWriterId": updated_writer_id}, status=200)
        except:
            return HttpResponse("Internal Server Error", status=500)
        

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
        Response: OK
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

        res = mongo.insert_message(guest_id, room_id, content)
        if res is not None:
            return JsonResponse({"Response": "OK"}, status=200)
        else:
            return HttpResponse("Internal Server error", status=500)

    return HttpResponse("Only POST requests are allowed", status=403)

