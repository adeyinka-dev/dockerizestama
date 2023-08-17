from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import TenantCreationForm
from accommodations.models import Room
from django.contrib.auth import login
