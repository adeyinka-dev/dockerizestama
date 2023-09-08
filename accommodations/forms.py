from django import forms
from .models import GeneralMessage


class GeneralMessageForm(forms.ModelForm):
    class Meta:
        model = GeneralMessage
        fields = ["title", "content"]
