from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from farm.models import Crop
from market.models import MarketPrice
from datetime import date, timedelta

Farmer = get_user_model()


class Command(BaseCommand):
    help = 'Seed initial data for the application'

    def handle(self, *args, **options):
        self.stdout.write('Seeding data...')
        
        # Create crops
        crops_data = [
            {
                'name': 'Rice',
                'variety': 'MR219',
                'optimal_temperature_min': 20,
                'optimal_temperature_max': 35,
                'optimal_moisture_min': 60,
                'optimal_moisture_max': 80,
                'optimal_humidity_min': 70,
                'optimal_humidity_max': 90,
                'growth_duration_days': 120,
                'description': 'Popular rice variety in Malaysia'
            },
            {
                'name': 'Corn',
                'variety': 'Sweet Corn',
                'optimal_temperature_min': 18,
                'optimal_temperature_max': 30,
                'optimal_moisture_min': 50,
                'optimal_moisture_max': 70,
                'optimal_humidity_min': 60,
                'optimal_humidity_max': 80,
                'growth_duration_days': 90,
                'description': 'Sweet corn variety'
            },
            {
                'name': 'Tomato',
                'variety': 'Local',
                'optimal_temperature_min': 18,
                'optimal_temperature_max': 28,
                'optimal_moisture_min': 60,
                'optimal_moisture_max': 80,
                'optimal_humidity_min': 50,
                'optimal_humidity_max': 70,
                'growth_duration_days': 75,
                'description': 'Local tomato variety'
            },
            {
                'name': 'Chili',
                'variety': 'Bird\'s Eye',
                'optimal_temperature_min': 20,
                'optimal_temperature_max': 32,
                'optimal_moisture_min': 50,
                'optimal_moisture_max': 70,
                'optimal_humidity_min': 60,
                'optimal_humidity_max': 80,
                'growth_duration_days': 90,
                'description': 'Spicy bird\'s eye chili'
            },
        ]
        
        for crop_data in crops_data:
            crop, created = Crop.objects.get_or_create(
                name=crop_data['name'],
                variety=crop_data['variety'],
                defaults=crop_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created crop: {crop.name}'))
            
            # Create sample market prices
            for i in range(10):
                price_date = date.today() - timedelta(days=i*7)
                price_value = 5.0 + (i * 0.5) + (hash(crop.name) % 10) * 0.1
                MarketPrice.objects.get_or_create(
                    crop=crop,
                    date=price_date,
                    defaults={
                        'price_per_kg': price_value,
                        'unit': 'MYR',
                        'source': 'Local Market',
                        'notes': f'Sample price data for {crop.name}'
                    }
                )
        
        self.stdout.write(self.style.SUCCESS('Data seeding completed!'))

