from django.db import models
from django.contrib.auth import get_user_model

Farmer = get_user_model()


class AdvisoryLog(models.Model):
    ADVISORY_TYPE_CHOICES = [
        ('irrigation', 'Irrigation'),
        ('fertilization', 'Fertilization'),
        ('pest_control', 'Pest Control'),
        ('harvest', 'Harvest'),
        ('other', 'Other'),
    ]
    
    advisory_id = models.AutoField(primary_key=True)
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='advisories')
    advisory_type = models.CharField(max_length=50, choices=ADVISORY_TYPE_CHOICES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    farm_plot = models.ForeignKey('farm.FarmPlot', on_delete=models.CASCADE, null=True, blank=True, related_name='advisories')
    crop = models.ForeignKey('farm.Crop', on_delete=models.CASCADE, null=True, blank=True, related_name='advisories')
    executed = models.BooleanField(default=False)
    executed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    priority = models.CharField(max_length=20, default='medium')
    
    class Meta:
        db_table = 'ADVISORY_LOG'
        verbose_name = 'Advisory Log'
        verbose_name_plural = 'Advisory Logs'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.farmer.username}"

