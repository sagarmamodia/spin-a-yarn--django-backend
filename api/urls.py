from django.urls import path
from . import views

urlpatterns = [
    path('api/create_room', views.create_room_view),
]