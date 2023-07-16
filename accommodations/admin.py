from django.contrib import admin
from .models import Hostel

# To see more informations about our Hostel


class HostelAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "address",
        "manager",
        "phone",
        "image",
    ]


admin.site.register(Hostel, HostelAdmin)
