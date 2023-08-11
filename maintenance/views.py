from django.shortcuts import render
from django.views.generic import DetailView
from .models import Maintenance


class RepairDetailView(DetailView):
    model = Maintenance
    template_name = "repair_detail.html"
