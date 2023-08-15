from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import TenantCreationForm, TenantChangeForm
from .models import Tenant
from accommodations.models import Room


class TenantAdmin(UserAdmin):
    add_form = TenantCreationForm
    form = TenantChangeForm
    model = Tenant
    list_display = [
        "username",
        "email",
        "first_name",
        "middle_initial",
        "last_name",
        "stama_id",
        "dob",
        "matric_num",
        "sex",
        "faculty",
        "department",
        "age",
        "is_staff",
        "user_image",
        "room_number",
        "hostel",
        "room_id",
        "rent_start_date",
        "rent_validity",
    ]

    readonly_fields = ("hostel",)

    fieldsets = UserAdmin.fieldsets + (
        (
            None,
            {
                "fields": (
                    "middle_initial",
                    "dob",
                    "sex",
                    "matric_num",
                    "faculty",
                    "department",
                    "user_image",
                    "phone_number",
                    "rent_start_date",
                )
            },
        ),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            None,
            {
                "fields": (
                    "room_id",
                    "dob",
                    "sex",
                    "matric_num",
                    "faculty",
                    "department",
                    "first_name",
                    "middle_initial",
                    "last_name",
                    "user_image",
                    "phone_number",
                    "rent_start_date",
                )
            },
        ),
    )

    # Overrode the save_model method in the form to automatically assign a tenant to a room based on the provided room_id and update the room's status to "Occupied".
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if "room_id" in form.cleaned_data:
            room_id = form.cleaned_data["room_id"]
            room = Room.objects.get(room_id=room_id)
            room.tenant = obj
            room.status = Room.OCCUPIED
            room.save()


admin.site.register(Tenant, TenantAdmin)
