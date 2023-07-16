from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.urls import reverse
import random


class Hostel(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=250)
    phone = models.IntegerField()
    amenities = models.TextField(max_length=9999)
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stama_id = models.CharField(max_length=12, unique=True, null=True, blank=True)
    # First Time I will be trying the image field
    image = models.ImageField(upload_to="hostels/", null=True, blank=True)

    def __str__(self):
        return self.name

    # This is to tell django to generate a URL for the hostel model. This will be used to generate the Hostel dashboard
    def get_absolute_url(self):
        return reverse("hostel_details", kwargs={"pk": self.pk})


@receiver(post_save, sender=Hostel)
def create_Hostel_id(sender, instance, created, **kwargs):
    # If a new Hostel instance has been created and the "stama_id" is empty
    if created and not instance.stama_id:
        # Random number between 1 and 9999
        # The resulting integer is formatted as a string, with leading zeros if necessary to ensure it's 5 digits long
        random_num = f"{random.randint(1, 100):04}"
        instance.stama_id = "STM/HSE/" + random_num
        instance.save()
