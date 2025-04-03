from django.urls import path
from . import views

urlpatterns = [
    path('create-room', views.create_room_view),
    path('submit-message', views.submit_message_view),
]