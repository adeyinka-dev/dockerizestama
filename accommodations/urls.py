from django.urls import path

from .views import HostelListView

urlpatterns = [
    path("", HostelListView.as_view(), name="hostel_list"),
]
