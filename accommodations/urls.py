from django.urls import path
from django.views.generic import TemplateView
from .views import HostelListView, HostelDetailView, RoomDetailView

urlpatterns = [
    path("<int:pk>/", HostelDetailView.as_view(), name="hostel_detail"),
    path("", HostelListView.as_view(), name="hostel_list"),
    path("room/<int:pk>/", RoomDetailView.as_view(), name="room_detail"),
    path(
        "submit_success/",
        TemplateView.as_view(template_name="submit_success.html"),
        name="submit_success",
    ),
]
