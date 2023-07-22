from django.views.generic import ListView, DetailView
from .models import Hostel


class HostelListView(ListView):
    model = Hostel
    template_name = "hostel_list.html"


class HostelDetailView(DetailView):
    model = Hostel
    template_name = "hostel_detail.html"
