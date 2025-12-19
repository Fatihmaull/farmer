from django.db import models
from farm.models import Crop


class MarketPrice(models.Model):
    price_id = models.AutoField(primary_key=True)
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='market_prices')
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=20, default='MYR')
    date = models.DateField()
    source = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'MARKET_PRICE'
        verbose_name = 'Market Price'
        verbose_name_plural = 'Market Prices'
        ordering = ['-date', '-created_at']
    
    def __str__(self):
        return f"{self.crop.name} - {self.price_per_kg} {self.unit} ({self.date})"

