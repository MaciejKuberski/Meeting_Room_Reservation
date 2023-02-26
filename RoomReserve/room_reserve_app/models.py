from django.db import models
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower

# Create your models here.
class Room(models.Model):
    room_name = models.CharField(max_length=255, unique=True)
    room_capacity = models.PositiveSmallIntegerField()
    projector_available = models.BooleanField()


class ReserveRoom(models.Model):
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    date = models.DateField()
    comment = models.CharField(max_length=255, null=True)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=[
                    'room_id', 'date'
                ],
                name='unique_booking') ]
