from django.contrib import admin
from .models import AdvisoryLog


@admin.register(AdvisoryLog)
class AdvisoryLogAdmin(admin.ModelAdmin):
    list_display = ('advisory_id', 'farmer', 'advisory_type', 'title', 'executed', 'created_at')
    list_filter = ('advisory_type', 'executed', 'created_at', 'priority')
    search_fields = ('title', 'message', 'farmer__username')
    readonly_fields = ('created_at',)

