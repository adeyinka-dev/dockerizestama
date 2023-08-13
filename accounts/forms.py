from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import DateField

from django_project import settings
from .models import Tenant


class TenantCreationForm(UserCreationForm):
    dob = DateField(input_formats=settings.DATE_FORMAT)

    class Meta:
        model = Tenant
        fields = UserCreationForm.Meta.fields + (
            "email",
            "first_name",
            "middle_initial",
            "last_name",
            "dob",
            "matric_num",
            "sex",
            "faculty",
            "department",
            "user_image",
            "phone_number",
        )


class TenantChangeForm(UserChangeForm):
    class Meta:
        model = Tenant
        fields = UserChangeForm.Meta.fields
