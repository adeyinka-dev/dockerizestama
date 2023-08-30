from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from .models import Hostel, Room
from maintenance.forms import MaintenanceForm
from maintenance.models import Maintenance
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
import math
from django.core.exceptions import PermissionDenied


class ManagerPermissionMixin:
    """
    Mixin that ensures that the logged-in user is the manager of the hostel or a superuser.
    """

    def dispatch(self, request, *args, **kwargs):
        hostel = self.get_object()
        # Check if the logged-in user is the manager of the hostel or a superuser
        if request.user == hostel.manager or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied


class HostelListView(ListView):
    def get(self, request, *args, **kwargs):
        hostels = Hostel.objects.filter(manager=request.user)
        return render(request, "hostel_list.html", {"hostels": hostels})


class StaffLoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "admin/admin_login.html")

    def post(self, request, *args, **kwargs):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect(reverse("hostel_list"))
        else:
            return render(
                request,
                "admin/admin_login.html",
                {"error": "Invalid login credentials"},
            )


class HostelDetailView(ManagerPermissionMixin, DetailView):
    model = Hostel
    template_name = "admin/hostel_dashboard.html"

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
        # Get Percentage
        total_rooms = rooms.count()
        occupied_rooms = rooms.filter(status=Room.OCCUPIED).count()
        unoccupied_rooms = rooms.filter(status=Room.UNOCCUPIED).count()
        unavailable_rooms = rooms.filter(status=Room.UNAVAILABLE).count()
        occupied_percentage = (
            math.ceil((occupied_rooms / total_rooms) * 100) if total_rooms else 0
        )
        unoccupied_percentage = (
            math.ceil((unoccupied_rooms / total_rooms) * 100) if total_rooms else 0
        )
        unavailable_percentage = (
            math.ceil((unavailable_rooms / total_rooms) * 100) if total_rooms else 0
        )
        context["total_rooms"] = total_rooms
        context["occupied_rooms"] = occupied_rooms
        context["unoccupied_rooms"] = unoccupied_rooms
        context["unavailable_rooms"] = unavailable_rooms
        context["occupied_percentage"] = occupied_percentage
        context["unoccupied_percentage"] = unoccupied_percentage
        context["unavailable_percentage"] = unavailable_percentage

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
    template_name = "admin/room_registry.html"

    def get_queryset(self):
        return Room.objects.filter(hostel__pk=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hostel"] = Hostel.objects.get(pk=self.kwargs["pk"])
        return context


class ResidentListView(ListView):
    model = Room
    template_name = "admin/resident_list.html"

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
