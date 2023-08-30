from django.urls import path
from django.views.generic import TemplateView
from .views import RoomRepair

urlpatterns = [
    path("room/<int:pk>/", RoomRepair.as_view(), name="raise_repair"),
    path(
        "submit_success/",
        TemplateView.as_view(template_name="submit_success.html"),
        name="submit_success",
    ),
]
