from typing import Any
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView, TemplateView, CreateView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from maintenance.models import Maintenance
from accommodations.models import Room
from accounts.forms import TenantCreationForm
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login


class HomePageView(RedirectView):
    def get_redirect_url(self, *args: Any, **kwargs):
        user = self.request.user
        # to check if user is authenticated
        if user.is_authenticated:
            # To check if user is staff
            if user.is_staff:
                return reverse("hostel_list")
            # Check if user has a room
            elif hasattr(user, "room") and user.room:
                return reverse("dashboard")
            # redirect to a room processing page if user has no room
            else:
                return reverse("processing")
        else:
            return reverse("auth")


class AuthPageView(TemplateView):
    template_name = "registration/auth.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["login_form"] = AuthenticationForm()
        context["register_form"] = UserCreationForm()
        return context


class Login(auth_views.LoginView):
    template_name = "registration/auth.html"
    success_url = reverse_lazy("home")


class SignUp(CreateView):
    template_name = "registration/auth.html"
    form_class = TenantCreationForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        # Save the tenant/user
        user = form.save()

        # Get the room using the provided room_id
        room_id = form.cleaned_data.get("room_id")
        room = Room.objects.get(room_id=room_id)

        # Assign the room to the user
        room.tenant = user
        room.status = Room.OCCUPIED  # Assuming you have this status defined
        room.save()

        # Log in the user and redirect to the success URL
        login(self.request, user)
        return super().form_valid(form)


class DashboardView(TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated and hasattr(user, "room") and user.room:
            context["repairs"] = Maintenance.objects.filter(room=user.room)
        return context


class ProcessingView(TemplateView):
    template_name = "processing.html"
