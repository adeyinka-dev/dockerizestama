from django.contrib import admin
from .models import Maintenance, MaintenanceType, MaintenanceSubType


class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ["hostel", "room", "type", "repair_id"]
    readonly_fields = ["hostel", "room", "repair_id"]
    # Filter
    list_filter = ["room__hostel", "type", "subtype"]


admin.site.register(Maintenance, MaintenanceAdmin)
admin.site.register(MaintenanceType)
admin.site.register(MaintenanceSubType)
