from django.contrib import admin
from .models import Maintenance, MaintenanceType, MaintenanceSubType


class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ["room", "type", "subtype", "repair_id"]


admin.site.register(Maintenance, MaintenanceAdmin)
admin.site.register(MaintenanceType)
admin.site.register(MaintenanceSubType)
