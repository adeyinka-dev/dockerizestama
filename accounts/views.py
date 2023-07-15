from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import TenantCreationForm


class SignUpView(CreateView):
    form_class = TenantCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
