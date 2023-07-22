from django.contrib import admin
from .models import Hostel, Room

# To see more informations about our Hostel


class RoomAdmin(admin.ModelAdmin):
    list_display = [
        "room_id",
        "room_number",
        "hostel",
        "tenant",
        "status",
    ]
    list_filter = ["hostel"]


class HostelAdmin(admin.ModelAdmin):
    list_display = ["name", "address", "manager", "phone", "image", "room_count"]


admin.site.register(Hostel, HostelAdmin)
admin.site.register(Room, RoomAdmin)
