from typing import Any, Dict
from django.db.models.query import QuerySet
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from .models import Hostel, Room
from maintenance.forms import MaintenanceForm
from django.apps import apps
from maintenance.models import Maintenance


class HostelListView(ListView):
    model = Hostel
    template_name = "hostels_list.html"


class HostelDetailView(DetailView):
    model = Hostel
    template_name = "hostel_dashboard.html"

    def get_context_data(self, **kwargs):
        """
        This method adds extra context data to the template.
        Specifically, it calculates the total number of rooms in the hostel,
        the number of occupied rooms and the number of unoccupied rooms.
        This context data can be used in the template to present these statistics to the user.
        It also includes a list of tenants with their first name, last name,
        and corresponding room number.
        This context data can be used in the template to present these statistics and
        tenant information to the user.
        """
        context = super().get_context_data(**kwargs)
        rooms = Room.objects.filter(hostel=self.object)
        context["total_rooms"] = rooms.count()
        context["occupied_rooms"] = rooms.filter(status=Room.OCCUPIED).count()
        context["unoccupied_rooms"] = rooms.filter(status=Room.UNOCCUPIED).count()
        context["unavailable_rooms"] = rooms.filter(status=Room.UNAVAILABLE).count()
        context["tenants"] = [
            {
                "first_name": room.tenant.first_name,
                "last_name": room.tenant.last_name,
                "room_number": room.room_number,
            }
            for room in rooms
            if room.tenant is not None
        ]

        # Repairs in each hostel
        repairs = Maintenance.objects.filter(room__in=rooms).order_by("-time_created")[
            :5
        ]
        pending_repairs = Maintenance.objects.filter(
            room__in=rooms, status=Maintenance.PENDING
        )
        inprogress_repairs = Maintenance.objects.filter(
            room__in=rooms, status=Maintenance.INPROGRESS
        )
        inspection_repairs = Maintenance.objects.filter(
            room__in=rooms, status=Maintenance.INSPECTION
        )
        completed_repairs = Maintenance.objects.filter(
            room__in=rooms, status=Maintenance.COMPLETED
        )
        context["pending_count"] = pending_repairs.count()
        context["inprogress_count"] = inprogress_repairs.count()
        context["inspection_count"] = inspection_repairs.count()
        context["completed_count"] = completed_repairs.count()
        context["repairs"] = repairs
        context["repairs_count"] = repairs.count()
        return context


class RoomListView(ListView):
    model = Room
    template_name = "room_list.html"

    def get_queryset(self):
        return Room.objects.filter(hostel__pk=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hostel"] = Hostel.objects.get(pk=self.kwargs["pk"])
        return context


class ResidentListView(ListView):
    model = Room
    template_name = "resident_list.html"

    def get_queryset(self):
        return Room.objects.filter(hostel__pk=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hostel"] = Hostel.objects.get(pk=self.kwargs["pk"])
        return context


class RoomDetailView(DetailView):
    model = Room
    template_name = "room_detail.html"

    # Django get_context_data method to allow forms to be accessed in the template.
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
