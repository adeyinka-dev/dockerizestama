from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import login
from django_project import settings
from .models import Tenant
from accommodations.models import Room
from django.contrib.auth.models import AbstractUser
from django.db import models


class ManagerProxy(Tenant):
    class Meta:
        proxy = True


class TenantCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label="password",
        strip=False,
        widget=forms.PasswordInput,
    )
    room_id = forms.CharField(max_length=20, required=False, label="Room ID")

    def __init__(self, *args, **kwargs):
        self.mode = kwargs.pop("mode", "tenant")  # default mode is 'tenant'
        super(TenantCreationForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Tenant
        fields = UserCreationForm.Meta.fields + (
            "username",
            "email",
            "room_id",
        )

    def clean_room_id(self):
        room_id = self.cleaned_data.get("room_id")

        # Only validate room_id if the form is in 'tenant' mode
        if self.mode == "tenant":
            try:
                room = Room.objects.get(room_id=room_id)
                if room.tenant:
                    raise forms.ValidationError("This room is already occupied.")
                if room.status != Room.UNOCCUPIED:
                    raise forms.ValidationError("This room is not available.")
            except Room.DoesNotExist:
                raise forms.ValidationError("This room ID does not exist.")
        return room_id


class TenantChangeForm(UserChangeForm):
    class Meta:
        model = Tenant
        fields = [
            "first_name",
            "last_name",
            "phone_number",
            "email",
            "matric_num",
            "department",
            "user_image",
            "dob",
            "department",
            "nok_name",
            "nok_phone",
        ]
