from django.shortcuts import render
from django.views.generic import DetailView
from .models import Maintenance


class RepairDetailView(DetailView):
    model = Maintenance
    template_name = "repair_detail.html"

    def get_template_names(self):
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            return ["repair_detail_fragment.html"]
        return ["repair_detail.html"]
