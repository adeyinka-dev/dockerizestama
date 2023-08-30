from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from .views import (
    HostelListView,
    HostelDetailView,
    RoomDetailView,
    RoomListView,
    ResidentListView,
    StaffLoginView,
)

urlpatterns = [
    path("hostel-list/", HostelListView.as_view(), name="hostel_list"),
    path("", StaffLoginView.as_view(), name="management"),
    path("<int:pk>/", HostelDetailView.as_view(), name="hostel_dashboard"),
    path("<int:pk>/rooms/", RoomListView.as_view(), name="room_list"),
    path("<int:pk>/residents/", ResidentListView.as_view(), name="resident_list"),
    path("room/<int:pk>/", RoomDetailView.as_view(), name="room_detail"),
    path(
        "submit_success/",
        TemplateView.as_view(template_name="submit_success.html"),
        name="submit_success",
    ),
    path(
        "management/logout/",
        auth_views.LogoutView.as_view(next_page="management"),
        name="admin_logout",
    ),
]
