from typing import Any, Dict
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import DetailView
from accommodations.models import Room
from django.core.mail import send_mail
import logging

logger = logging.getLogger(__name__)


class RoomRepair(LoginRequiredMixin, UserPassesTestMixin, DetailView):
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
            room = self.get_object()
            maintenance.room = room
            maintenance.save()
            hostel_email = room.hostel.email
            if hostel_email:
                try:
                    send_mail(
                        "Room Repair Requested",
                        "A tenant has raised a repair request.",
                        "makindeyinkax@gmail.com",
                        [hostel_email],
                        fail_silently=False,
                    )
                except Exception as e:
                    logger.error(f"Failed to send email. Error: {e}")

            return redirect("submit_success")
        return self.get(request, *args, **kwargs)

    def test_func(self):
        room = self.get_object()
        return room.tenant == self.request.user
