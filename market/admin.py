from django.contrib import admin
from .models import MarketPrice


@admin.register(MarketPrice)
class MarketPriceAdmin(admin.ModelAdmin):
    list_display = ('price_id', 'crop', 'price_per_kg', 'unit', 'date', 'source')
    list_filter = ('date', 'crop', 'unit')
    search_fields = ('crop__name', 'source')
    date_hierarchy = 'date'

