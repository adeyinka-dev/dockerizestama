from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import TenantCreationForm, TenantChangeForm
from .models import Tenant


class TenantAdmin(UserAdmin):
    add_form = TenantCreationForm
    form = TenantChangeForm
    model = Tenant
    list_display = [
        "email",
        "username",
        "stama_id",
        "dob",
        "matric_num",
        "sex",
        "faculty",
        "department",
        "age",
        "is_staff",
    ]
    fieldsets = UserAdmin.fieldsets + (
        (
            None,
            {"fields": ("dob", "sex", "matric_num", "faculty", "department")},
        ),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            None,
            {"fields": ("dob", "sex", "matric_num", "faculty", "department")},
        ),
    )


admin.site.register(Tenant, TenantAdmin)
