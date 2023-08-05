from django.db import models
from accommodations.models import Room

""" Instead of hardcoding different types and subtypes of repair, I created a general and """
""" seperate models for them linking them with foreign keys"""
""" I can then easily add the various types of repairs on the admin page"""


# This model represents the primary type of maintenance, for example, Electrical, Plumbing, carpentry etc.


class MaintenanceType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# This model represents the subtype of maintenance, for example, under "Electrical" you might have "Socket", "Light", etc.


class MaintenanceSubType(models.Model):
    name = models.CharField(max_length=50)
    type = models.ForeignKey(MaintenanceType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# The actual model which is associated with each room and shows the tyoe of repair needed


class Maintenance(models.Model):
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="repairs",
    )
    location = models.CharField(
        max_length=20,
        null=True,
        blank=True,
    )
    type = models.ForeignKey(
        MaintenanceType,
        on_delete=models.CASCADE,
        related_name="repairs",
    )
    subtype = models.ForeignKey(
        MaintenanceSubType,
        on_delete=models.CASCADE,
        related_name="repair",
        null=True,
        blank=True,
    )
    is_pending = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Operative to attend to{self.type}, subtype: {self.subtype} at: {self.room.hostel}, room: {self.room.room_number}"
