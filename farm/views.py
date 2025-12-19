from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count, Avg
from django.utils import timezone
from datetime import timedelta
from .models import FarmPlot, Crop, PlantingRecord, SensorData
from .forms import FarmPlotForm, PlantingRecordForm, SensorDataForm
from advisory.models import AdvisoryLog


@login_required
def dashboard(request):
    farmer = request.user
    plots = FarmPlot.objects.filter(farmer=farmer)
    total_plots = plots.count()
    
    active_plantings = PlantingRecord.objects.filter(
        farm_plot__farmer=farmer,
        status__in=['planted', 'growing']
    )
    active_crops = active_plantings.values('crop').distinct().count()
    
    latest_advisories = AdvisoryLog.objects.filter(
        farmer=farmer,
        executed=False
    ).order_by('-created_at')[:5]
    
    latest_sensor_data = SensorData.objects.filter(
        farm_plot__farmer=farmer
    ).order_by('-recorded_at')[:5]
    
    active_plantings_with_crops = active_plantings.select_related('crop')
    price_summary = []
    for planting in active_plantings_with_crops:
        from market.models import MarketPrice
        latest_price = MarketPrice.objects.filter(
            crop=planting.crop
        ).order_by('-date').first()
        if latest_price:
            price_summary.append({
                'crop': planting.crop.name,
                'price': latest_price.price_per_kg,
                'unit': latest_price.unit
            })
    
    context = {
        'total_plots': total_plots,
        'active_crops': active_crops,
        'latest_advisories': latest_advisories,
        'latest_sensor_data': latest_sensor_data,
        'price_summary': price_summary,
    }
    return render(request, 'farm/dashboard.html', context)


@login_required
def plot_list(request):
    plots = FarmPlot.objects.filter(farmer=request.user)
    return render(request, 'farm/plot_list.html', {'plots': plots})


@login_required
def plot_create(request):
    if request.method == 'POST':
        form = FarmPlotForm(request.POST)
        if form.is_valid():
            plot = form.save(commit=False)
            plot.farmer = request.user
            plot.save()
            messages.success(request, 'Farm plot created successfully!')
            return redirect('plot_list')
    else:
        form = FarmPlotForm()
    return render(request, 'farm/plot_form.html', {'form': form, 'title': 'Create Farm Plot'})


@login_required
def plot_detail(request, pk):
    plot = get_object_or_404(FarmPlot, pk=pk, farmer=request.user)
    planting_records = plot.planting_records.all()
    sensor_data = list(plot.sensor_data.all()[:30])
    
    import json
    sensor_chart_data = {
        'labels': json.dumps([sd.recorded_at.strftime('%Y-%m-%d %H:%M') for sd in sensor_data]),
        'moisture': json.dumps([float(sd.moisture) if sd.moisture else 0 for sd in sensor_data]),
        'temperature': json.dumps([float(sd.temperature) if sd.temperature else 0 for sd in sensor_data]),
        'humidity': json.dumps([float(sd.humidity) if sd.humidity else 0 for sd in sensor_data]),
    }
    
    context = {
        'plot': plot,
        'planting_records': planting_records,
        'sensor_data': sensor_data,
        'sensor_chart_data': sensor_chart_data,
    }
    return render(request, 'farm/plot_detail.html', context)


@login_required
def plot_edit(request, pk):
    plot = get_object_or_404(FarmPlot, pk=pk, farmer=request.user)
    if request.method == 'POST':
        form = FarmPlotForm(request.POST, instance=plot)
        if form.is_valid():
            form.save()
            messages.success(request, 'Farm plot updated successfully!')
            return redirect('plot_detail', pk=plot.pk)
    else:
        form = FarmPlotForm(instance=plot)
    return render(request, 'farm/plot_form.html', {'form': form, 'title': 'Edit Farm Plot', 'plot': plot})


@login_required
def plot_delete(request, pk):
    plot = get_object_or_404(FarmPlot, pk=pk, farmer=request.user)
    if request.method == 'POST':
        plot.delete()
        messages.success(request, 'Farm plot deleted successfully!')
        return redirect('plot_list')
    return render(request, 'farm/plot_confirm_delete.html', {'plot': plot})


@login_required
def planting_record_create(request):
    if request.method == 'POST':
        form = PlantingRecordForm(request.POST, farmer=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Planting record created successfully!')
            return redirect('planting_record_list')
    else:
        form = PlantingRecordForm(farmer=request.user)
    return render(request, 'farm/planting_record_form.html', {'form': form, 'title': 'Add Planting Record'})


@login_required
def planting_record_list(request):
    records = PlantingRecord.objects.filter(farm_plot__farmer=request.user)
    return render(request, 'farm/planting_record_list.html', {'records': records})


@login_required
def sensor_data_create(request):
    if request.method == 'POST':
        form = SensorDataForm(request.POST, farmer=request.user)
        if form.is_valid():
            sensor_data = form.save()
            from advisory.views import generate_advisory
            generate_advisory(request.user, sensor_data)
            messages.success(request, 'Sensor data added successfully! Advisory generated if needed.')
            return redirect('sensor_data_list')
    else:
        form = SensorDataForm(farmer=request.user)
    return render(request, 'farm/sensor_data_form.html', {'form': form, 'title': 'Add Sensor Data'})


@login_required
def sensor_data_list(request):
    plot_id = request.GET.get('plot')
    sensor_data = SensorData.objects.filter(farm_plot__farmer=request.user)
    if plot_id:
        sensor_data = sensor_data.filter(farm_plot_id=plot_id)
    sensor_data = sensor_data.order_by('-recorded_at')[:50]
    
    plots = FarmPlot.objects.filter(farmer=request.user)
    
    context = {
        'sensor_data': sensor_data,
        'plots': plots,
        'selected_plot': int(plot_id) if plot_id else None,
    }
    return render(request, 'farm/sensor_data_list.html', context)


@login_required
def knowledge_base(request):
    return render(request, 'farm/knowledge_base.html')

