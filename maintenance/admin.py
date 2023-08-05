from django.contrib import admin

from .models import Maintenance, MaintenanceType, MaintenanceSubType


admin.site.register(Maintenance)
admin.site.register(MaintenanceType)
admin.site.register(MaintenanceSubType)
