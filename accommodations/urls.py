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
    RepairListView,
    RepairDetailView,
    OperativeListView,
    GeneralMessageCreateView,
    GeneralMessageListView,
    GeneralMessageDetailView,
    GeneralMessageDeleteView,
)

urlpatterns = [
    path("hostel-list/", HostelListView.as_view(), name="hostel_list"),
    path("", StaffLoginView.as_view(), name="management"),
    path("<int:pk>/", HostelDetailView.as_view(), name="hostel_dashboard"),
    path("<int:pk>/rooms/", RoomListView.as_view(), name="room_list"),
    path("maintenance/<int:pk>/", RepairDetailView.as_view(), name="work_detail"),
    path("<int:pk>/repairs/", RepairListView.as_view(), name="repairs_registry"),
    path("<int:pk>/residents/", ResidentListView.as_view(), name="resident_list"),
    path("room/<int:pk>/", RoomDetailView.as_view(), name="room_detail"),
    # General Message URL start
    path(
        "hostel/<int:pk>/create_message/",
        GeneralMessageCreateView.as_view(),
        name="create_message",
    ),
    path(
        "hostel/<int:pk>/general_message/",
        GeneralMessageListView.as_view(),
        name="general_message",
    ),
    path(
        "hostel/<int:pk>/general_message/message_detail",
        GeneralMessageDetailView.as_view(),
        name="message_detail",
    ),
    path(
        "hostel/<int:pk>/general_message/<int:message_pk>/delete/",
        GeneralMessageDeleteView.as_view(),
        name="message_delete",
    ),
    path("operatives/<int:pk>", OperativeListView.as_view(), name="operative_list"),
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
