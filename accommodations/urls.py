from django.urls import path

from .views import HostelListView, HostelDetailView

urlpatterns = [
    path("<int:pk>/", HostelDetailView.as_view(), name="hostel_detail"),
    path("", HostelListView.as_view(), name="hostel_list"),
]
