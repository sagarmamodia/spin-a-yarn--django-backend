from django.urls import path
from . import views

urlpatterns = [
    path('create-room/', views.create_room_view),
    path('submit-message/', views.submit_message_view),
    path('join-room/', views.join_room_view),
    path('get-random-room/', views.get_random_room_view),
    path('get-all-messages/<str:room_id>/', views.get_all_messages_view),
    path('get-participants/<str:room_id>/', views.get_room_participants),
    path('update-current-writer/', views.update_current_writer_view),
    path('join-room/', views.join_room_view),
]