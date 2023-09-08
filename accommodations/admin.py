from django.contrib import admin
from .models import Hostel, Room, Operative, GeneralMessage
from accounts.models import Tenant

# To see more informations about our Hostel


class OperativeAdmin(admin.ModelAdmin):
    list_display = ["full_name", "speciality", "contact"]


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
    # Manage Field can only be ffrom user with is_staff status active
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "manager":
            kwargs["queryset"] = Tenant.objects.filter(is_staff=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    list_display = ["name", "address", "manager", "phone", "image", "room_count"]


class GeneralMessageAdmin(admin.ModelAdmin):
    list_display = ["title", "content", "author"]


admin.site.register(GeneralMessage, GeneralMessageAdmin)


admin.site.register(Operative)
admin.site.register(Hostel, HostelAdmin)
admin.site.register(Room, RoomAdmin)
