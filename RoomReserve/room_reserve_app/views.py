from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
# Create your views here.

class HomePage(View):
    def get(self, request):
        return render(request, 'home.html')


class RoomList(View):
    def get(self,request):
        return render(request, 'room-list.html')


class NewRoom(View):
    def get(self,request):
        return render(request, 'add-new-room.html')