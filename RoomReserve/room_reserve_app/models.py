from django.db import models

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
        unique_together = ('room_id','date')

