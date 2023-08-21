from django.urls import path
from django.views.generic import TemplateView
from .views import RepairDetailView, RoomRepair

urlpatterns = [
    path(
        "maintenance/repair/<int:pk>/", RepairDetailView.as_view(), name="work_detail"
    ),
    path("room/<int:pk>/", RoomRepair.as_view(), name="raise_repair"),
    path(
        "submit_success/",
        TemplateView.as_view(template_name="submit_success.html"),
        name="submit_success",
    ),
]
