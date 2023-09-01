from django import forms
from .models import Client


class ClientCreationForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            "hostel_name",
            "address",
            "message",
            "contact_name",
            "email",
            "phone",
        ]
