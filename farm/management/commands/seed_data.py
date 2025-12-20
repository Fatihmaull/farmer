import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import transaction
from faker import Faker

# Import Model
from farm.models import Crop, FarmPlot, PlantingRecord, SensorData
from advisory.models import AdvisoryLog
from market.models import MarketPrice

Farmer = get_user_model()

# GUNAKAN DEFAULT (Aman dari Error Locale)
fake = Faker() 

class Command(BaseCommand):
    help = "Seed realistic Malaysia agriculture data (Safe Mode)"

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("🇲🇾 STARTING MALAYSIA SEEDING (Safe Mode)..."))

        # ======================
        # 1. CROPS (Malaysia Spec)
        # ======================
        crops_data = [
            ("Padi", "MR297 (Siraj)"),
            ("Padi", "MR269"),
            ("Kelapa Sawit", "Tenera (DxP)"),
            ("Getah", "RRIM 3001"),
            ("Durian", "Musang King (D197)"),
            ("Durian", "Black Thorn (D200)"),
            ("Harumanis", "Mango MA 128"),
            ("Cili", "Kulai"),
            ("Nanas", "MD2"),
        ]

        crops = []
        for name, variety in crops_data:
            crop, created = Crop.objects.get_or_create(
                name=name,
                variety=variety,
                defaults={
                    "optimal_temperature_min": random.randint(24, 26),
                    "optimal_temperature_max": random.randint(32, 36),
                    "optimal_moisture_min": random.randint(60, 75),
                    "optimal_moisture_max": random.randint(85, 95),
                    "optimal_humidity_min": random.randint(70, 80),
                    "optimal_humidity_max": random.randint(90, 100),
                    "growth_duration_days": random.randint(100, 150),
                    "description": fake.paragraph(nb_sentences=2),
                },
            )
            crops.append(crop)
        
        self.stdout.write(self.style.SUCCESS(f"✅ Crops ready: {len(crops)} types"))

        # ======================
        # 2. FARMERS (Users)
        # ======================
        farmers = []
        self.stdout.write("... Creating farmers")
        
        for _ in range(10): 
            # Pakai nama random (international) agar tidak error locale
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = f"{first_name.lower()}{random.randint(1,999)}"
            email = f"{username}@farmer.com"
            
            if not Farmer.objects.filter(username=username).exists():
                farmer = Farmer.objects.create_user(
                    username=username,
                    email=email,
                    password="password123"
                )
                farmer.first_name = first_name
                farmer.last_name = last_name
                farmer.save()
                farmers.append(farmer)

        existing_users = list(Farmer.objects.all())
        farmers = list(set(farmers + existing_users))

        self.stdout.write(self.style.SUCCESS(f"✅ Farmers pool: {len(farmers)} users"))

        # ======================
        # 3. FARM PLOTS (Hardcoded Malaysia Locations)
        # ======================
        plots = []
        soil_choices = ['clay', 'sandy', 'loamy', 'silty', 'peat', 'chalky']
        
        # KITA PAKSA PAKAI LIST INI AGAR TERLIHAT MALAYSIA
        # Tanpa menggunakan fake.city() yang bisa error/keluar nama kota US
        locations_malaysia = [
            "Changlun, Kedah", "Bukit Kayu Hitam, Kedah", "Jitra, Kedah", 
            "Arau, Perlis", "Kangar, Perlis", "Sintok, Kedah", 
            "Alor Setar, Kedah", "Kubang Pasu, Kedah", "Pendang, Kedah",
            "Padang Besar, Perlis", "Kuala Nerang, Kedah", "Pokok Sena, Kedah"
        ]

        self.stdout.write("... Creating plots")
        for farmer in farmers:
            for _ in range(random.randint(1, 3)):
                # Ambil acak dari list Malaysia di atas
                loc = random.choice(locations_malaysia)

                plot = FarmPlot.objects.create(
                    farmer=farmer,
                    location=loc,
                    size_hectares=round(random.uniform(0.5, 10.0), 2),
                    soil_type=random.choice(soil_choices),
                )
                plots.append(plot)
        
        self.stdout.write(self.style.SUCCESS(f"✅ Created {len(plots)} Farm Plots"))

        # ======================
        # 4. PLANTING RECORDS
        # ======================
        plantings = []
        self.stdout.write("... Creating planting records")

        for plot in plots:
            crop = random.choice(crops)
            plant_date = fake.date_between(start_date="-1y", end_date="today")
            growth_days = crop.growth_duration_days or 90
            expected_harvest = plant_date + timedelta(days=growth_days)

            planting = PlantingRecord(
                farm_plot=plot,
                crop=crop,
                planting_date=plant_date,
                expected_harvest_date=expected_harvest,
                expected_yield_kg=round(random.uniform(2000, 10000), 2),
                actual_yield_kg=random.choice([None, round(random.uniform(1500, 9000), 2)]),
                status='growing' if expected_harvest > date.today() else 'harvested',
                notes=fake.sentence(),
            )
            plantings.append(planting)

        PlantingRecord.objects.bulk_create(plantings)
        self.stdout.write(self.style.SUCCESS(f"✅ Created {len(plantings)} Planting Records"))

        # ======================
        # 5. SENSOR DATA (Tropical)
        # ======================
        sensor_bulk = []
        self.stdout.write("... Generating tropical sensor data")
        now = timezone.now()
        
        for plot in plots:
            # 50 data per plot
            for i in range(50): 
                record_time = now - timedelta(hours=i*6)
                sensor_bulk.append(
                    SensorData(
                        farm_plot=plot,
                        recorded_at=record_time,
                        # Suhu Tropis (24-34 C)
                        temperature=round(random.uniform(24, 34), 2),
                        # Lembap
                        moisture=round(random.uniform(60, 95), 2),
                        humidity=round(random.uniform(70, 98), 2),
                        ph_level=round(random.uniform(5.5, 7.0), 2),
                        notes="Auto reading"
                    )
                )

        batch_size = 1000
        for i in range(0, len(sensor_bulk), batch_size):
            SensorData.objects.bulk_create(sensor_bulk[i:i + batch_size])
            
        self.stdout.write(self.style.SUCCESS(f"✅ {len(sensor_bulk)} Sensor Data rows created"))

        # ======================
        # 6. ADVISORY LOGS
        # ======================
        advisories = []
        advisory_types = ['irrigation', 'fertilization', 'pest_control', 'harvest', 'other']
        
        self.stdout.write("... Creating advisory logs")

        for plot in plots:
            for _ in range(random.randint(1, 3)):
                is_exec = random.choice([True, False])
                adv_type = random.choice(advisory_types)

                advisories.append(
                    AdvisoryLog(
                        farmer=plot.farmer,
                        farm_plot=plot,
                        crop=random.choice(crops),
                        advisory_type=adv_type,
                        title=f"{adv_type.replace('_', ' ').title()} Alert",
                        message=fake.sentence(),
                        executed=is_exec,
                        executed_at=timezone.now() if is_exec else None,
                        priority=random.choice(['low', 'medium', 'high']),
                    )
                )
        
        AdvisoryLog.objects.bulk_create(advisories)
        self.stdout.write(self.style.SUCCESS(f"✅ {len(advisories)} Advisory logs created"))

        # ======================
        # 7. MARKET PRICES (MYR)
        # ======================
        prices = []
        self.stdout.write("... Generating MYR market history")
        
        # Sumber data hardcoded agar terlihat Malaysia
        sources = ["Pasar Borong Kedah", "FAMA", "Local Wholesaler", "Pasar Tani Changlun"]

        for crop in crops:
            base_price = random.randint(5, 40)
            for i in range(60): 
                prices.append(
                    MarketPrice(
                        crop=crop,
                        date=date.today() - timedelta(days=i),
                        price_per_kg=round(base_price + random.uniform(-2, 2), 2),
                        unit="MYR",
                        source=random.choice(sources),
                        notes="Daily average"
                    )
                )
        
        MarketPrice.objects.bulk_create(prices)
        self.stdout.write(self.style.SUCCESS(f"✅ {len(prices)} Market Price points created"))

        self.stdout.write(self.style.SUCCESS("🚀 SEEDING COMPLETED SUCCESSFULLY!"))