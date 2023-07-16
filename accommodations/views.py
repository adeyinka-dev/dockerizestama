from django.views.generic import ListView
from .models import Hostel


class HostelListView(ListView):
    model = Hostel
    template_name = "hostel_list.html"
