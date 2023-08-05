from django import forms
from .models import Maintenance


class MaintenaceForm(forms.ModelForm):
    class Meta:
        model = Maintenance
        fields = ["type", "subtype", "description", "location"]
