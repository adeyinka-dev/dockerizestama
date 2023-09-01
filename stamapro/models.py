from django.db import models


class Client(models.Model):
    class ServiceStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        CONTACTED = "contacted", "Contacted"
        ACCEPTED = "accepted", "Accepted"
        VERIFIED = "verified", "Verified"
        APPROVED = "approved", "Approved"
        CANCELLED = "cancelled", "Cancelled"

    hostel_name = models.CharField(max_length=200)
    address = models.TextField(null=True, blank=True)
    number_of_rooms = models.PositiveIntegerField(null=True, blank=True)
    additional_features = models.TextField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)

    contact_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    date_submitted = models.DateTimeField(auto_now_add=True)
    service_status = models.CharField(
        max_length=20, choices=ServiceStatus.choices, default=ServiceStatus.PENDING
    )

    def __str__(self):
        return f"{self.hostel_name} - {self.contact_name} ({self.service_status})"
