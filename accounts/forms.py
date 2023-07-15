from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Tenant


class TenantCreationForm(UserCreationForm):
    class Meta:
        model = Tenant
        fields = UserCreationForm.Meta.fields + (
            "email",
            "dob",
            "matric_num",
            "sex",
            "faculty",
            "department",
        )


class TenantChangeForm(UserChangeForm):
    class Meta:
        model = Tenant
        fields = UserChangeForm.Meta.fields
