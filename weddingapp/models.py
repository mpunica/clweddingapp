"""
Django models for coderslab app.
"""
from django.db import models

BrideGroom_choice = (
    (0, "Bride"),
    (1, "Groom"),
)
class BrideGroom(models.Model):
    name = models.CharField(max_length=64)
    BrideGroom = models.IntegerField(choices=BrideGroom_choice)

    def __str__(self):
        return f"{self.name}"

class Guest(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    is_child = models.BooleanField()
    bridegrooms = models.ForeignKey(BrideGroom, on_delete=models.CASCADE)
    in_confirmed = models.BooleanField()

    @property
    def name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def __str__(self):
        return self.name

# class GuestFrom(models.Model):
#     Guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
#     BrideGroom_from = models.ForeignKey(BrideGroom, on_delete=models.CASCADE)
#     BrideGroom_choice = models.FloatField(choices=BrideGroom_choice)

class Present(models.Model):
    present_name = models.CharField(max_length=64)
    guests = models.ManyToManyField(Guest)
    price = models.DecimalField(decimal_places=2, max_digits=8)

# class PresentReservation(models.Model):
#     guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
#     present = models.ForeignKey(Present, on_delete=models.CASCADE)

class SeatTable(models.Model):
    table_nr = models.IntegerField()
    place_nr = models.IntegerField()
    guests = models.OneToOneField(Guest, on_delete=models.CASCADE)

class Messages(models.Model):
    guests = models.ForeignKey(Guest, on_delete=models.CASCADE)
    message = models.CharField(max_length=64)
