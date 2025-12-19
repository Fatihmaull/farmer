# Smart Agriculture Support System (SASS)

A web-based system to help smallholder farmers in Changlun manage farm plots, crops, sensor data, advisory recommendations, market prices, and farming records.

## Tech Stack

- Backend: Python Django 4.2.7
- Frontend: Django Templates + Bootstrap 5
- Database: MySQL
- ORM: Django ORM
- Charts: Chart.js
- Authentication: Django Auth (custom Farmer model)
- Environment: .env support

## Setup Instructions

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Database**
   - Create a MySQL database
   - Copy `.env.example` to `.env`
   - Update database credentials in `.env`:
     ```
     DB_NAME=farmer_db
     DB_USER=root
     DB_PASSWORD=your-password
     DB_HOST=localhost
     DB_PORT=3306
     SECRET_KEY=your-secret-key-here
     DEBUG=True
     ```

3. **Run Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create Superuser (Optional)**
   ```bash
   python manage.py createsuperuser
   ```

5. **Seed Initial Data (Optional)**
   ```bash
   python manage.py seed_data
   ```

6. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

7. **Access the Application**
   - Open browser: http://127.0.0.1:8000/
   - Register a new farmer account or login

## Features

- **Authentication**: Register and login as farmer
- **Dashboard**: Overview of farm plots, crops, advisories, and sensor data
- **Farm Plot Management**: CRUD operations for farm plots
- **Planting Records**: Track crop planting and harvest data
- **Sensor Data**: Input and view sensor readings with charts
- **Advisory System**: Auto-generated recommendations based on sensor data
- **Market Prices**: View current and historical crop prices
- **Knowledge Base**: Farming tips and best practices

## Project Structure

```
sass/
├── auth_app/          # Authentication app with custom Farmer model
├── farm/              # Farm plots, crops, planting records, sensor data
├── advisory/          # Advisory recommendation system
├── market/            # Market price information
├── templates/         # HTML templates
├── static/            # Static files (CSS, JS, images)
└── sass/              # Project settings
```

## Database Schema

- FARMER: Custom user model
- FARM_PLOT: Farm plot information
- CROP: Crop types with optimal growth parameters
- PLANTING_RECORD: Planting and harvest records
- SENSOR_DATA: Environmental sensor readings
- ADVISORY_LOG: Generated advisory recommendations
- MARKET_PRICE: Market price data

## Notes

- The system automatically generates advisories when sensor data is added
- Advisories compare sensor values with crop optimal growth data
- All pages are mobile-responsive using Bootstrap 5
- Charts are rendered using Chart.js

