from django.shortcuts import redirect, render
from django.views.generic import DetailView
from .models import Maintenance
from accommodations.models import Room
from .forms import MaintenanceForm


class RepairDetailView(DetailView):
    model = Maintenance
    template_name = "repair_detail.html"


class RoomRepair(DetailView):
    model = Room
    template_name = "raise_repair.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = MaintenanceForm()
        return context

    def post(self, request, *args, **kwargs):
        form = MaintenanceForm(request.POST)
        if form.is_valid():
            maintenance = form.save(commit=False)
            maintenance.room = self.get_object()
            maintenance.save()
            return redirect("submit_success")
        return self.get(request, *args, **kwargs)
