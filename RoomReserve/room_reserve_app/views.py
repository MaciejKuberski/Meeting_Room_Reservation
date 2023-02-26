from django.shortcuts import render, redirect, reverse, HttpResponseRedirect
from django.http import HttpResponse
from django.views import View
from .models import Room, ReserveRoom
from django.db import IntegrityError, DataError
from datetime import datetime, date, timedelta
from django.contrib import messages

# Create your views here.


rooms = Room.objects.all().values_list()
today = date.today()
def redirect_room_list():
    return redirect("http://127.0.0.1:8000/room/list")
# Define a class-based view for the home page
class HomePage(View):
    """
    Renders the home page
    """
    def get(self, request):
        """
        GET request method for rendering the home page
        """
        return render(request, 'home.html')


# Define a class-based view for the room list
class RoomList(View):
    """
    Renders the list of all available rooms or a message if there are no rooms
    """
    def get(self, request):
        """
        GET request method for rendering the list of all available rooms or a message if there are no rooms
        """
        # Get all rooms from the database
        rooms = Room.objects.all().values_list()

        # If there are rooms, render the room list with the rooms context
        if rooms:
            room_booking_data = ReserveRoom.objects.all().values_list()
            room_booking_id_list = [x[1] for x in list(room_booking_data)]
            room_booking_id_set = set(room_booking_id_list)
            room_booking_date_list = [[x[1],x[2]] for x in list(room_booking_data)]
            room_booking_dict = {}
            for elem in room_booking_date_list:
                if elem[0] in room_booking_dict:
                    room_booking_dict[elem[0]].append(elem[1])
                else:
                    room_booking_dict[elem[0]] = [elem[1]]

            ctx = {"rooms": rooms,
                   "today": today,
                   "room_booking_id_list": room_booking_id_list,
                   "room_booking_date_list": room_booking_date_list,
                   "room_booking_id_set":room_booking_id_set,
                   "room_booking_dict":room_booking_dict,
                   }
            return render(request, "room-list.html", ctx)
        # If there are no rooms, render the room list with a message context
        else:
            ctx = {"message": "No rooms available"}
            return render(request, "room-list.html", ctx)


# Define a class-based view for adding a new room
class NewRoom(View):
    """
    Renders the form for adding a new room and adds the room to the database
    """
    def get(self, request):
        """
        GET request method for rendering the form for adding a new room
        """
        return render(request, 'new-room.html')

    def post(self, request):
        """
        POST request method for adding a new room to the database
        """
        # Get room information from the request
        room_name = request.POST.get('room_name')
        room_capacity = request.POST.get('room_capacity', )
        projector_available = request.POST.get('projector_available', 'no')

        try:
            # Check if the room capacity is a positive integer
            if int(room_capacity) > 0:
                # Create a new room with the room information
                Room.objects.create(room_name=room_name,
                                     room_capacity=room_capacity,
                                     projector_available=projector_available)
                # Render the new-room page with a success message
                ctx = {"message": "Room Added!"}
                return render(request, 'new-room.html', ctx)
            else:
                # Render the new-room page with an error message if the room capacity is not a positive integer
                ctx = {"message": "Capacity needs to be a positive number and cannot be 0"}
                return render(request, 'new-room.html', ctx)

        # Catch errors if the room information is not valid
        except (IntegrityError, ValueError, DataError):
            # Render the new-room page with an error message
            ctx = {"message": "Wrong Input, room was NOT added, possible reasons:",
                   "reasons": ("Fields cannot be empty","Room with that name already exists",
                               "Capacity cannot be higher than 32767 ")}
            return render(request, 'new-room.html', ctx)





class DeleteRoom(View):
    """
    A view that deletes a room with the given ID.
    """
    def get(self, request, room_id):
        """
        Deletes a room with the given ID.
        """
        Room.objects.filter(pk=room_id).delete()
        redirect_room_list()


class ModifyRoom(View):
    """
    A view that modifies a room with the given ID.
    """
    def get(self, request, room_id):
        """
        Renders the modify-room.html template with the room data for the given ID.
        """
        room = Room.objects.filter(pk = room_id).values_list()
        ctx = {"room" : room}
        return render(request, "modify-room.html", ctx)

    def post(self, request, room_id):
        """
        Updates the room data for the given ID with the submitted data.
        """
        new_room_name = request.POST.get('room_name')
        new_room_capacity = request.POST.get('room_capacity')
        new_projector_available = request.POST.get('projector_available')
        old_room_name_object = Room.objects.filter(pk = room_id).values_list()
        old_room_name_tuple = old_room_name_object[0]
        old_room_name = old_room_name_tuple[1]

        try:
            if int(new_room_capacity) > 0:
                if old_room_name == new_room_name:
                    Room.objects.filter(pk=room_id).update(room_name=new_room_name, room_capacity=new_room_capacity,
                                                           projector_available=new_projector_available)
                    messages.success(request, "Changes made successfully")
                    redirect_room_list()

                else:
                    if not Room.objects.filter(room_name = new_room_name):
                        Room.objects.filter(pk = room_id).update(room_name = new_room_name, room_capacity = new_room_capacity,
                                                                 projector_available = new_projector_available)

                        messages.success(request, "Changes made successfully")
                        redirect_room_list()


                    else:
                        messages.success(request, "Name already reserved!")
                        redirect_room_list()

            else:
                messages.success(request, "Capacity needs to be a positive  number and cannot be 0")
                redirect_room_list()

        except (IntegrityError, ValueError, DataError):
            messages.success(request, "Changes were not made. Possible reasons: empty fields, name taken, "
                               "max capacity exceeded, capacity not a positive number or 0")
            redirect_room_list()



def future_date(given_date):
    """
    Returns True if the given date is in the future, False otherwise.
    """
    compare_date = datetime.strptime(given_date,"%Y-%m-%d")
    return datetime.today() <= compare_date + timedelta(days=1)

class ReservingRoom(View):
    def get(self, request, room_id):
        """
        Render the reservation form.

        Args:
            request: A request object.
            room_id (int): The ID of the room to reserve.

        Returns:
            A rendered HTTP response with the reservation form.
        """
        room_name_object = Room.objects.filter(id=room_id).values_list()
        room_name_tuple = room_name_object[0]
        room_name = room_name_tuple[1]
        ctx = {"message": room_name}
        return render(request, "reserve-room.html", ctx)

    def post(self, request, room_id):
        """
        Handle reservation form submission.

        Args:
            request: A request object.
            room_id (int): The ID of the room to reserve.

        Returns:
            A rendered HTTP response with the result of the reservation attempt.
        """
        room_name_object = Room.objects.filter(id=room_id).values_list()
        room_name_tuple = room_name_object[0]
        room_name = room_name_tuple[1]
        reservation_date = request.POST.get('room_date')
        comment = request.POST.get('room_comment')

        try:
            if future_date(reservation_date) or reservation_date == today:
                ReserveRoom.objects.create(date=reservation_date, comment=comment, room_id_id=room_id)

                messages.success(request, "You have successfully reserved room !")
                return HttpResponseRedirect(reverse('room-list'))


            else:
                messages.success(request, "Reservation failed, reservation date in the past")
                return HttpResponseRedirect(reverse('room-list'))


        except IntegrityError:
            messages.success(request, "Room already reserved on that date")
            return HttpResponseRedirect(reverse('room-list'))



class ShowRoom(View):
    def get(self, request, room_id):
        """
        Handle GET requests to the view.

        Args:
            request (HttpRequest): The HTTP request object.
            room_id (int): The ID of the room to display details for.

        Returns:
            An HTTP response object containing the rendered template with the room details.
        """
        # Retrieve the room object from the database
        room_object = Room.objects.filter(id=room_id).values_list()
        room_tuple = room_object[0]

        # Extract the relevant details from the room tuple
        selected_room_id = room_tuple[0]
        selected_room_name = room_tuple[1]
        selected_room_capacity = room_tuple[2]
        selected_room_projector = room_tuple[3]

        # Retrieve the booking data for the selected room
        booking_data = ReserveRoom.objects.filter(room_id_id=room_id).values_list()
        booking_data_list = list(booking_data)
        booking_data_days = [x[2] for x in booking_data_list]

        # Generate a list of dates for the next seven days, starting from today

        next_seven_days = [date.today() + timedelta(days=x) for x in range(7)]

        # Build the context dictionary to pass to the template
        ctx = {
            "selected_room_id": selected_room_id,
            "selected_room_name": selected_room_name,
            "selected_room_capacity": selected_room_capacity,
            "selected_room_projector": selected_room_projector,
            "booking_data": booking_data,
            "today": today,
            "next_seven_days": next_seven_days,
            "booking_data_days": booking_data_days,
        }

        # Render the template with the context dictionary and return the HTTP response
        return render(request, "show-room.html", ctx)


