from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, FormView
from .models import Hostel, Room, Operative
from maintenance.forms import MaintenanceForm, MaintenanceStatusForm, NoteForm
from maintenance.models import Maintenance
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
import math
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse


class ManagerPermissionMixin:
    """
    Mixin that ensures that the logged-in user is the manager of the hostel or a superuser.
    """

    def dispatch(self, request, *args, **kwargs):
        if isinstance(self, DetailView):
            obj = self.get_object()
        elif isinstance(self, ListView):
            obj = self.get_queryset().first()
        elif isinstance(self, View):
            obj = Maintenance.objects.get(pk=self.kwargs["pk"])
        else:
            raise ValueError("ManagerPermissionMixin used in an inappropriate view")
        # Check if the object is a Room and reference the manager of its related Hostel
        if isinstance(obj, Room):
            manager = obj.hostel.manager
        elif isinstance(obj, Maintenance):
            manager = obj.room.hostel.manager
        else:
            manager = obj.manager
        if request.user == manager or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied


class HostelListView(ManagerPermissionMixin, ListView):
    model = Hostel
    template_name = "hostel_list.html"
    context_object_name = "hostels"

    def get_queryset(self):
        """
        Override the get_queryset method to filter hostels by the logged-in manager.
        """
        return Hostel.objects.filter(manager=self.request.user)


class OperativeListView(ListView):
    model = Operative
    template_name = "management/operative_list.html"
    context_object_name = "operatives"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hostel"] = Hostel.objects.get(pk=self.kwargs.get("pk"))
        return context


class StaffLoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "registration/admin_login.html")

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
                "registration/admin_login.html",
                {"error": "Invalid login credentials"},
            )


class HostelDetailView(ManagerPermissionMixin, DetailView):
    model = Hostel
    template_name = "management/hostel_dashboard.html"

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
        # Nofication to show only last 3 pending maintnance request
        nofity_repairs = Maintenance.objects.filter(
            room__in=rooms, status=Maintenance.PENDING
        ).order_by("-time_created")[:3]
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
        context["notify_repairs"] = nofity_repairs
        context["repairs_count"] = repairs.count()
        return context


class RoomListView(ManagerPermissionMixin, ListView):
    model = Room
    template_name = "management/room_registry.html"

    def get_queryset(self):
        return Room.objects.filter(hostel__pk=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hostel"] = Hostel.objects.get(pk=self.kwargs["pk"])
        return context


class ResidentListView(ManagerPermissionMixin, ListView):
    model = Room
    template_name = "management/resident_list.html"

    def get_queryset(self):
        return Room.objects.filter(hostel__pk=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hostel"] = Hostel.objects.get(pk=self.kwargs["pk"])
        return context


class RoomDetailView(ManagerPermissionMixin, DetailView):
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


class RepairListView(ManagerPermissionMixin, ListView):
    model = Maintenance
    template_name = "management/repair_list.html"

    def get_queryset(self):
        return Maintenance.objects.filter(room__hostel__pk=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hostel"] = Hostel.objects.get(pk=self.kwargs["pk"])
        return context

    def get_object(self):
        # Override the get_object method to return the related Hostel object
        return Hostel.objects.get(pk=self.kwargs["pk"])


class NoteGet(DetailView):
    model = Maintenance
    template_name = "management/work_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = NoteForm()
        context["status_form"] = MaintenanceStatusForm(instance=self.object)
        return context


class PostNote(FormView):
    model = Maintenance
    form_class = NoteForm
    template_name = "management/work_detail.html"

    def get_maintenance(self):
        return Maintenance.objects.get(pk=self.kwargs["pk"])

    def get_success_url(self):
        maintenance = self.object
        return reverse("work_detail", kwargs={"pk": maintenance.pk})

    def post(self, request, *args, **kwargs):
        self.object = self.get_maintenance()

        # Check if status form was submitted
        status_form = MaintenanceStatusForm(request.POST, instance=self.object)
        if status_form.is_valid():
            status_form.save()
            return JsonResponse(
                {"status": "success", "message": "Status updated successfully!"}
            )

        # If status form wasn't submitted, continue with the note processing
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        note = form.save(commit=False)
        note.maintenance = self.object
        note.author = self.request.user
        note.save()
        data = {
            "status": "success",
            "message": "Note added successfully!",
            "note": {
                "author": str(note.author),
                "content": str(note),
                "time_added": note.time_added.strftime("%B %d, %Y, %I:%M %p"),
            },
        }
        return JsonResponse(data)

    def form_invalid(self, form):
        return JsonResponse(
            {"status": "error", "message": "There was an error processing the form."},
            status=400,
        )

    def post(self, request, *args, **kwargs):
        self.object = self.get_maintenance()

        # Check if status form was submitted
        status_form = MaintenanceStatusForm(request.POST, instance=self.object)
        if status_form.is_valid():
            status_form.save()
            return redirect(self.get_success_url())  # Redirect to the detail page

        # If status form wasn't submitted, continue with the note processing
        return super().post(request, *args, **kwargs)


class RepairDetailView(ManagerPermissionMixin, View):
    def get(self, request, *args, **kwargs):
        view = NoteGet.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PostNote.as_view()
        return view(request, *args, **kwargs)
