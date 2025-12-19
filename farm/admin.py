from django.contrib import admin
from .models import FarmPlot, Crop, PlantingRecord, SensorData


@admin.register(FarmPlot)
class FarmPlotAdmin(admin.ModelAdmin):
    list_display = ('plot_id', 'farmer', 'location', 'size_hectares', 'soil_type', 'created_at')
    list_filter = ('soil_type', 'created_at')
    search_fields = ('location', 'farmer__username')


@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ('crop_id', 'name', 'variety', 'growth_duration_days')
    search_fields = ('name', 'variety')


@admin.register(PlantingRecord)
class PlantingRecordAdmin(admin.ModelAdmin):
    list_display = ('record_id', 'farm_plot', 'crop', 'planting_date', 'status', 'expected_yield_kg', 'actual_yield_kg')
    list_filter = ('status', 'planting_date')
    search_fields = ('crop__name', 'farm_plot__location')


@admin.register(SensorData)
class SensorDataAdmin(admin.ModelAdmin):
    list_display = ('data_id', 'farm_plot', 'temperature', 'moisture', 'humidity', 'recorded_at')
    list_filter = ('recorded_at',)
    search_fields = ('farm_plot__location',)

