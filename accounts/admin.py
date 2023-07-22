from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import TenantCreationForm, TenantChangeForm
from .models import Tenant


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
    ]
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
                )
            },
        ),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            None,
            {
                "fields": (
                    "dob",
                    "sex",
                    "matric_num",
                    "faculty",
                    "department",
                    "first_name",
                    "middle_initial",
                    "last_name",
                    "user_image",
                )
            },
        ),
    )


admin.site.register(Tenant, TenantAdmin)
