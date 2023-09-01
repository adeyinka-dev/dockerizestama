from django.utils import timezone
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import login
from django_project import settings
from .models import Tenant
from accommodations.models import Room
from django.db import models


class ManagerProxy(Tenant):
    class Meta:
        proxy = True


class TenantCreationForm(UserCreationForm):
    """Custom form for tenant registration.

    - Extends the built-in UserCreationForm.
    - Has an optional mode ('tenant' by default) to determine validation logic.
    - Contains an additional field, `room_id`, to capture tenant's room.
    - Validates the room based on its availability and existence.
    - Upon tenant sign-up, the `rent_start_date` in the Tenant model is set to the current date.
    """

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

    def save(self, commit=True):
        """
        Override the default save method to handle rent start date.
        """
        # First, call the parent's save method to save the Tenant object.
        tenant = super(TenantCreationForm, self).save(commit=False)

        # I  Handled the rent start date logic here
        room_id = self.cleaned_data.get("room_id")
        if self.mode == "tenant" and room_id:
            try:
                room = Room.objects.get(room_id=room_id)
                tenant.rent_start_date = timezone.now().date()

                # If commit is True, save tenant and update room
                if commit:
                    tenant.save()
                    room.tenant = tenant  # Link the room to the tenant
                    room.save()

            except Room.DoesNotExist:
                # This should not happen as validation should catch it, but it's good to be safe lol!.
                raise ValueError("This room ID does not exist.")
        elif commit:
            tenant.save()  # Save tenant even if not in 'tenant' mode

        return tenant


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


class ManagerChnageForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = [
            "first_name",
            "last_name",
            "phone_number",
            "email",
            "user_image",
        ]
