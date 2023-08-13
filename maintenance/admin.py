from django.contrib import admin
from .models import Maintenance, MaintenanceType, MaintenanceSubType, Note


class NoteInline(admin.StackedInline):
    model = Note
    extra = 0


class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ["hostel", "room", "type", "repair_id"]
    readonly_fields = ["hostel", "room", "repair_id"]
    # Filter
    list_filter = ["room__hostel", "type", "subtype"]
    inlines = [
        NoteInline,
    ]


admin.site.register(Maintenance, MaintenanceAdmin)
admin.site.register(MaintenanceType)
admin.site.register(MaintenanceSubType)
admin.site.register(Note)
