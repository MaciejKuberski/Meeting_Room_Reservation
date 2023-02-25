from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import View
from room_reserve_app.models import Room
from django.db import IntegrityError, DataError

# Create your views here.


class HomePage(View):
    def get(self, request):
        return render(request, 'home.html')


class RoomList(View):
    def get(self,request):
        rooms = Room.objects.all().values_list()
        if rooms:
            ctx = {"rooms":rooms}
            return render(request, "room-list.html", ctx)
        else:
            ctx = {"message": "No rooms available"}
            return render(request, "room-list.html", ctx)


class NewRoom(View):
    def get(self,request):
        return render(request, 'new-room.html')

    def post(self,request):
        room_name = request.POST.get('room_name')
        room_capacity = request.POST.get('room_capacity', )
        projector_available = request.POST.get('projector_available', 'no')


        try:
            if int(room_capacity) > 0:
                Room.objects.create(room_name = room_name,
                                room_capacity = room_capacity,
                                projector_available = projector_available)
                ctx = {"message": "Room Added!"}
                return render(request, 'new-room.html', ctx)
            else:
                ctx = {"message": "Capacity needs to be a positive  number and cannot be 0"}
                return render(request, 'new-room.html', ctx)

        except (IntegrityError, ValueError, DataError):
            ctx = {"message": "Wrong Input, room was NOT added, possible reasons:",
                   "reasons": ("Fields cannot be empty","Room with that name already exists",
                               "Capacity cannot be higher than 32767 ")}
            return render(request, 'new-room.html', ctx)




class DeleteRoom(View):
    def get(self, request, room_id):
        Room.objects.filter(pk=room_id).delete()
        return redirect('http://127.0.0.1:8000/room/list')


class ModifyRoom(View):
    def get(self, request, room_id):
        room = Room.objects.filter(pk = room_id).values_list()
        ctx = {"room" : room}
        return render(request, "modify-room.html", ctx)
    def post(self, request, room_id):

        new_room_name = request.POST.get('room_name')
        new_room_capacity = request.POST.get('room_capacity')
        new_projector_available = request.POST.get('projector_available')
        rooms = Room.objects.all().values_list()

        try:
            if int(new_room_capacity) > 0:
                Room.objects.filter(pk = room_id).update(room_name = new_room_name, room_capacity = new_room_capacity,
                                                         projector_available = new_projector_available)
                ctx = {"message" : "Changes made successfully",
                       "rooms":rooms}
                return render(request,"room-list.html", ctx)
            else:
                ctx = {"message": "Capacity needs to be a positive  number and cannot be 0"}
                return render(request, 'room-list.html', ctx)

        except (IntegrityError, ValueError, DataError):
            ctx = {"message" : "Changes were not made. Possible reasons: empty fields, name taken, "
                               "max capacity exceeded, capacity not a positive number or 0",
                   "rooms":rooms}
            return render(request, "room-list.html", ctx)

