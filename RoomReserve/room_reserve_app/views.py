from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from room_reserve_app.models import Room
from django.db import IntegrityError

# Create your views here.


class HomePage(View):
    def get(self, request):
        return render(request, 'home.html')


class RoomList(View):
    def get(self,request):
        return render(request, 'room-list.html')


class NewRoom(View):
    def get(self,request):
        return render(request, 'new-room.html')

    def post(self,request):
        room_name = request.POST.get('room_name')
        room_capacity = request.POST.get('room_capacity', 1)
        projector_available = request.POST.get('projector_available', 'no')

        try:
            Room.objects.create(room_name = room_name,
                            room_capacity = room_capacity,
                            projector_available = projector_available)
            ctx = {"message": "Room Added!"}
            return render(request, 'new-room.html', ctx)

        except (IntegrityError, ValueError):
            ctx = {"message": "Wrong Input, room was NOT added, possible reasons:",
                   "reasons": ("Fields cannot be empty","Room with that name already exists",
                               "Wrong capacity (number needs to be positive, not higher than 32767)",)}
            return render(request, 'new-room.html', ctx)

