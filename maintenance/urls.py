from django.urls import path
from .views import RepairDetailView

urlpatterns = [
    path(
        "maintenance/repair/<int:pk>/", RepairDetailView.as_view(), name="repair_detail"
    ),
]
