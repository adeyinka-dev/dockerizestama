from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from accommodations.models import Room
import random

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
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="repairs")
    location = models.CharField(max_length=20, null=True, blank=True)
    type = models.ForeignKey(
        MaintenanceType, on_delete=models.CASCADE, related_name="repairs"
    )
    subtype = models.ForeignKey(
        MaintenanceSubType,
        on_delete=models.CASCADE,
        related_name="repairs",
        null=True,
        blank=True,
    )
    repair_id = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True,
    )
    is_pending = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Operative to attend to{self.type}, subtype: {self.subtype} at: {self.room.hostel}, room: {self.room.room_number}"

    # Funtion to generate a repair unique ID, that will be used for repair search.


@receiver(post_save, sender=Maintenance)
def create_repair_id(sender, instance, created, **kwargs):
    if created and not instance.repair_id:
        random_num = f"{random.randint(1, 1000):04}"
        instance.repair_id = "REP" + random_num
        instance.save()
