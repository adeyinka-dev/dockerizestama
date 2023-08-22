from django import forms
from .models import Maintenance, Note


class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = Maintenance
        fields = ["type", "subtype", "description", "location"]


class MaintenanceStatusForm(forms.ModelForm):
    class Meta:
        model = Maintenance
        fields = ["status"]


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ("note",)
