from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import login
from django_project import settings
from .models import Tenant
from accommodations.models import Room


class TenantCreationForm(UserCreationForm):
    # Set django to only take one password input
    password1 = forms.CharField(
        label="password",
        strip=False,
        widget=forms.PasswordInput,
    )
    # Added a room_id field to the form for room assignment during tenant/user creation.
    room_id = forms.CharField(max_length=20, required=True, label="Room ID")

    class Meta:
        model = Tenant
        fields = UserCreationForm.Meta.fields + (
            "username",
            "email",
            "department",
            "room_id",
        )

    # Implemented validation in clean_room_id to ensure the provided room_id exists, is unoccupied, and is available before a tenant is assigned.
    def clean_room_id(self):
        room_id = self.cleaned_data.get("room_id")
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
        fields = UserChangeForm.Meta.fields
