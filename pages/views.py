from typing import Any, Dict
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import views as auth_views
from django.views.generic import (
    RedirectView,
    TemplateView,
    CreateView,
    UpdateView,
    ListView,
)
from maintenance.models import Maintenance, Room
from accommodations.models import Room
from accounts.models import Tenant
from accounts.forms import TenantCreationForm, TenantChangeForm
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login
from django.db import transaction


class HomePageView(RedirectView):
    def get_redirect_url(self, *args: Any, **kwargs):
        user = self.request.user
        # to check if user is authenticated
        if user.is_authenticated:
            return reverse("dashboard")
            # redirect to a room processing page if user has no room
        else:
            return reverse("login")


class Login(auth_views.LoginView):
    template_name = "registration/login.html"
    success_url = reverse_lazy("home")


class SignUp(CreateView):
    template_name = "registration/signup.html"
    form_class = TenantCreationForm
    success_url = reverse_lazy("register_success")

    @transaction.atomic
    def form_valid(self, form):
        # Save the user
        user = form.save(commit=False)  # Dont save yet, will save on line 66
        user.save()
        # Get the room using the provided room_id
        try:
            room_id = form.cleaned_data.get("room_id")
            room = Room.objects.select_for_update().get(room_id=room_id)
            # Check if the room is already occupied
            if room.status == Room.OCCUPIED:
                form.add_error("room_id", "This room is already occupied")
                return self.form_invalid(form)
            # Assign the room to the user
            room.tenant = user
            room.status = Room.OCCUPIED  # Assuming you have this status defined
            room.save()

            # Log in the user and redirect to the success URL
            login(self.request, user)
            return super().form_valid(form)
        except Room.DoesNotExist:
            form.add_error("room_id", "Room with this ID does not exist")
            return self.form_invalid(form)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "user_dashboard.html"


class RepairHistoryView(LoginRequiredMixin, ListView):
    model = Maintenance
    template_name = "repair_history.html"
    context_object_name = "repairs"

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and hasattr(user, "room") and user.room:
            return Maintenance.objects.filter(room=user.room)
        return Maintenance.objects.none()


class EditInfo(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Tenant
    template_name = "update_profile.html"
    form_class = TenantChangeForm

    def get_success_url(self):
        return reverse("update_success")

    def test_func(self):
        return self.get_object() == self.request.user


class TestPage(TemplateView):
    template_name = "admin/base.html"
