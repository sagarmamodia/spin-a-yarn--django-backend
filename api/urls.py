from django.urls import path
from . import views

urlpatterns = [
    path('create-room/', views.create_room_view),
    path('submit-message/', views.submit_message_view),
    path('join-room/', views.join_room_view),
    path('get-random-room/', views.get_random_room_view),
    path('get-all-messages/', views.get_all_messages_view),
    path('get-participants/', views.get_room_participants),
    path('get-current-writer/', views.get_current_writer),
    path('join-room/', views.join_room_view),
]