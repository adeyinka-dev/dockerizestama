from typing import Any, Dict
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from .models import Hostel, Room
from maintenance.forms import MaintenaceForm


class HostelListView(ListView):
    model = Hostel
    template_name = "hostel_list.html"


class HostelDetailView(DetailView):
    model = Hostel
    template_name = "hostel_detail.html"

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
        context["unoccupied_rooms"] = context["total_rooms"] - context["occupied_rooms"]
        context["tenants"] = [
            {
                "first_name": room.tenant.first_name,
                "last_name": room.tenant.last_name,
                "room_number": room.room_number,
            }
            for room in rooms
            if room.tenant is not None
        ]
        return context


class RoomDetailView(DetailView):
    model = Room
    template_name = "room_detail.html"

    # Django get_context_data method to allow forms to be accessed in the template.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = MaintenaceForm()
        return context

    def post(self, request, *args, **kwargs):
        form = MaintenaceForm(request.POST)
        if form.is_valid():
            maintenance = form.save(commit=False)
            maintenance.room = self.get_object()
            maintenance.save()
            return redirect("submit_success")
        return self.get(request, *args, **kwargs)
