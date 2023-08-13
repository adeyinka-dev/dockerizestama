from typing import Any
from django.views.generic import RedirectView, TemplateView
from maintenance.models import Maintenance
from django.urls import reverse, reverse_lazy


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
            return reverse("login")


class LoginView(TemplateView):
    template_name = "registration/login.html"
    success_url = reverse_lazy("home")


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
