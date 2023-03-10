"""RoomReserve URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from room_reserve_app.views import HomePage, RoomList, NewRoom, DeleteRoom, ModifyRoom, ReservingRoom, ShowRoom

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePage.as_view()),
    path('room/list/', RoomList.as_view(), name='room-list'),
    path('room/new/', NewRoom.as_view()),
    path('room/delete/<int:room_id>', DeleteRoom.as_view()),
    path('room/modify/<int:room_id>', ModifyRoom.as_view()),
    path('room/reserve/<int:room_id>' ,ReservingRoom.as_view()),
    path('room/show/<int:room_id>', ShowRoom.as_view()),
]
