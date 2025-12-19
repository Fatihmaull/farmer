from django.db import models
from django.contrib.auth import get_user_model

Farmer = get_user_model()


class FarmPlot(models.Model):
    SOIL_TYPE_CHOICES = [
        ('clay', 'Clay'),
        ('sandy', 'Sandy'),
        ('loamy', 'Loamy'),
        ('silty', 'Silty'),
        ('peat', 'Peat'),
        ('chalky', 'Chalky'),
    ]
    
    plot_id = models.AutoField(primary_key=True)
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='farm_plots')
    location = models.CharField(max_length=255)
    size_hectares = models.DecimalField(max_digits=10, decimal_places=2)
    soil_type = models.CharField(max_length=50, choices=SOIL_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'FARM_PLOT'
        verbose_name = 'Farm Plot'
        verbose_name_plural = 'Farm Plots'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.location} ({self.size_hectares} ha)"


class Crop(models.Model):
    crop_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    variety = models.CharField(max_length=100, blank=True)
    optimal_temperature_min = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    optimal_temperature_max = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    optimal_moisture_min = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    optimal_moisture_max = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    optimal_humidity_min = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    optimal_humidity_max = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    growth_duration_days = models.IntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'CROP'
        verbose_name = 'Crop'
        verbose_name_plural = 'Crops'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.variety})" if self.variety else self.name


class PlantingRecord(models.Model):
    STATUS_CHOICES = [
        ('planted', 'Planted'),
        ('growing', 'Growing'),
        ('harvested', 'Harvested'),
        ('failed', 'Failed'),
    ]
    
    record_id = models.AutoField(primary_key=True)
    farm_plot = models.ForeignKey(FarmPlot, on_delete=models.CASCADE, related_name='planting_records')
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='planting_records')
    planting_date = models.DateField()
    expected_harvest_date = models.DateField(null=True, blank=True)
    actual_harvest_date = models.DateField(null=True, blank=True)
    expected_yield_kg = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    actual_yield_kg = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planted')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'PLANTING_RECORD'
        verbose_name = 'Planting Record'
        verbose_name_plural = 'Planting Records'
        ordering = ['-planting_date']
    
    def __str__(self):
        return f"{self.crop.name} - {self.farm_plot.location} ({self.planting_date})"


class SensorData(models.Model):
    data_id = models.AutoField(primary_key=True)
    farm_plot = models.ForeignKey(FarmPlot, on_delete=models.CASCADE, related_name='sensor_data')
    temperature = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    moisture = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    humidity = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    ph_level = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        db_table = 'SENSOR_DATA'
        verbose_name = 'Sensor Data'
        verbose_name_plural = 'Sensor Data'
        ordering = ['-recorded_at']
    
    def __str__(self):
        return f"{self.farm_plot.location} - {self.recorded_at}"

