from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import AdvisoryLog
from farm.models import SensorData, Crop, PlantingRecord


def generate_advisory(farmer, sensor_data):
    plot = sensor_data.farm_plot
    active_planting = PlantingRecord.objects.filter(
        farm_plot=plot,
        status__in=['planted', 'growing']
    ).first()
    
    if not active_planting:
        return None
    
    crop = active_planting.crop
    advisories = []
    
    if sensor_data.moisture is not None and crop.optimal_moisture_min and crop.optimal_moisture_max:
        if float(sensor_data.moisture) < float(crop.optimal_moisture_min):
            advisories.append({
                'type': 'irrigation',
                'title': 'Low Soil Moisture Detected',
                'message': f'Soil moisture ({sensor_data.moisture}%) is below optimal range ({crop.optimal_moisture_min}-{crop.optimal_moisture_max}%). Please irrigate the field.',
                'priority': 'high'
            })
        elif float(sensor_data.moisture) > float(crop.optimal_moisture_max):
            advisories.append({
                'type': 'irrigation',
                'title': 'High Soil Moisture Detected',
                'message': f'Soil moisture ({sensor_data.moisture}%) is above optimal range. Consider reducing irrigation.',
                'priority': 'medium'
            })
    
    if sensor_data.temperature is not None and crop.optimal_temperature_min and crop.optimal_temperature_max:
        if float(sensor_data.temperature) < float(crop.optimal_temperature_min):
            advisories.append({
                'type': 'other',
                'title': 'Low Temperature Alert',
                'message': f'Temperature ({sensor_data.temperature}°C) is below optimal range ({crop.optimal_temperature_min}-{crop.optimal_temperature_max}°C). Consider protective measures.',
                'priority': 'medium'
            })
        elif float(sensor_data.temperature) > float(crop.optimal_temperature_max):
            advisories.append({
                'type': 'other',
                'title': 'High Temperature Alert',
                'message': f'Temperature ({sensor_data.temperature}°C) is above optimal range. Ensure adequate irrigation.',
                'priority': 'high'
            })
    
    if sensor_data.humidity is not None and crop.optimal_humidity_min and crop.optimal_humidity_max:
        if float(sensor_data.humidity) < float(crop.optimal_humidity_min):
            advisories.append({
                'type': 'irrigation',
                'title': 'Low Humidity Alert',
                'message': f'Air humidity ({sensor_data.humidity}%) is below optimal range. Consider increasing irrigation frequency.',
                'priority': 'medium'
            })
        elif float(sensor_data.humidity) > float(crop.optimal_humidity_max):
            advisories.append({
                'type': 'pest_control',
                'title': 'High Humidity Alert',
                'message': f'High humidity ({sensor_data.humidity}%) may promote fungal growth. Monitor for diseases.',
                'priority': 'medium'
            })
    
    for adv in advisories:
        AdvisoryLog.objects.create(
            farmer=farmer,
            advisory_type=adv['type'],
            title=adv['title'],
            message=adv['message'],
            farm_plot=plot,
            crop=crop,
            priority=adv['priority']
        )
    
    return advisories


@login_required
def advisory_list(request):
    advisories = AdvisoryLog.objects.filter(farmer=request.user)
    executed_filter = request.GET.get('executed')
    if executed_filter == 'true':
        advisories = advisories.filter(executed=True)
    elif executed_filter == 'false':
        advisories = advisories.filter(executed=False)
    
    advisories = advisories.order_by('-created_at')
    return render(request, 'advisory/advisory_list.html', {'advisories': advisories})


@login_required
def advisory_detail(request, pk):
    advisory = get_object_or_404(AdvisoryLog, pk=pk, farmer=request.user)
    return render(request, 'advisory/advisory_detail.html', {'advisory': advisory})


@login_required
def advisory_execute(request, pk):
    advisory = get_object_or_404(AdvisoryLog, pk=pk, farmer=request.user)
    if request.method == 'POST':
        advisory.executed = True
        advisory.executed_at = timezone.now()
        advisory.save()
        messages.success(request, 'Advisory marked as executed!')
        return redirect('advisory_list')
    return render(request, 'advisory/advisory_execute.html', {'advisory': advisory})

