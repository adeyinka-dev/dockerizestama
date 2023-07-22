from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.urls import reverse
import random  # Imported tenant from the account app.
from accounts.models import Tenant


class Hostel(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=250)
    phone = models.IntegerField()
    amenities = models.TextField(max_length=9999)
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stama_id = models.CharField(max_length=12, unique=True, null=True, blank=True)
    # First Time I will be trying the image field
    image = models.ImageField(upload_to="hostels/", null=True, blank=True)
    room_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    # This is to tell django to generate a URL for the hostel model. This will be used to generate the Hostel dashboard
    def get_absolute_url(self):
        return reverse("hostel_detail", kwargs={"pk": self.pk})


@receiver(post_save, sender=Hostel)
def create_Hostel_id(sender, instance, created, **kwargs):
    # If a new Hostel instance has been created and the "stama_id" is empty
    if created and not instance.stama_id:
        # Random number between 1 and 9999
        # The resulting integer is formatted as a string, with leading zeros if necessary to ensure it's 5 digits long
        random_num = f"{random.randint(1, 100):04}"
        instance.stama_id = "STM/HSE/" + random_num
        instance.save()


@receiver(post_save, sender=Hostel)
def create_rooms(sender, instance, **kwargs):
    # If hostel is created or room_count is updated
    existing_room_count = instance.rooms.count()
    if existing_room_count < instance.room_count:
        # If the current number of rooms is less than room_count, create new rooms
        for i in range(existing_room_count + 1, instance.room_count + 1):
            Room.objects.create(hostel=instance, room_number=str(i).zfill(3))
    elif existing_room_count > instance.room_count:
        # If the current number of rooms is more than room_count, keep existing rooms, don't delete
        pass


# Room model (This will be chnage to FLat model in case this was created for block of flats)


class Room(models.Model):
    # room divided to 3 different status. For statistics purpose on admin dashboard
    OCCUPIED = "OC"
    UNOCCUPIED = "UC"
    UNAVAILABLE = "UNAV"
    ROOM_STATUS = [
        (OCCUPIED, "Occupied"),
        (UNOCCUPIED, "Unoccupied"),
        (UNAVAILABLE, "Unavailable"),
    ]
    room_id = models.CharField(max_length=20, unique=True)
    room_number = models.CharField(max_length=3)
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name="rooms")
    tenant = models.OneToOneField(
        Tenant, on_delete=models.SET_NULL, null=True, blank=True
    )
    status = models.CharField(max_length=20, choices=ROOM_STATUS, default=UNOCCUPIED)

    def __str__(self):
        return self.room_id


# room unique ID, will take the hostel id and consecutive numbers will be added.
@receiver(post_save, sender=Room)
def create_room_id(sender, instance, created, **kwargs):
    if created and not instance.room_id:
        room_number = f"{instance.pk:03}"
        instance.room_id = instance.hostel.stama_id + "/RM/" + instance.room_number
        instance.save(update_fields=["room_id"])
