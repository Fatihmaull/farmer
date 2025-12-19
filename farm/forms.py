from django import forms
from .models import FarmPlot, Crop, PlantingRecord, SensorData


class FarmPlotForm(forms.ModelForm):
    class Meta:
        model = FarmPlot
        fields = ['location', 'size_hectares', 'soil_type']
        widgets = {
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'size_hectares': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'soil_type': forms.Select(attrs={'class': 'form-control'}),
        }


class CropForm(forms.ModelForm):
    class Meta:
        model = Crop
        fields = ['name', 'variety', 'optimal_temperature_min', 'optimal_temperature_max',
                  'optimal_moisture_min', 'optimal_moisture_max', 'optimal_humidity_min',
                  'optimal_humidity_max', 'growth_duration_days', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'variety': forms.TextInput(attrs={'class': 'form-control'}),
            'optimal_temperature_min': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'optimal_temperature_max': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'optimal_moisture_min': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'optimal_moisture_max': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'optimal_humidity_min': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'optimal_humidity_max': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'growth_duration_days': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class PlantingRecordForm(forms.ModelForm):
    class Meta:
        model = PlantingRecord
        fields = ['farm_plot', 'crop', 'planting_date', 'expected_harvest_date',
                  'expected_yield_kg', 'notes']
        widgets = {
            'farm_plot': forms.Select(attrs={'class': 'form-control'}),
            'crop': forms.Select(attrs={'class': 'form-control'}),
            'planting_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'expected_harvest_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'expected_yield_kg': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        farmer = kwargs.pop('farmer', None)
        super().__init__(*args, **kwargs)
        if farmer:
            self.fields['farm_plot'].queryset = FarmPlot.objects.filter(farmer=farmer)


class SensorDataForm(forms.ModelForm):
    class Meta:
        model = SensorData
        fields = ['farm_plot', 'temperature', 'moisture', 'humidity', 'ph_level', 'notes']
        widgets = {
            'farm_plot': forms.Select(attrs={'class': 'form-control'}),
            'temperature': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'moisture': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'humidity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'ph_level': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        farmer = kwargs.pop('farmer', None)
        super().__init__(*args, **kwargs)
        if farmer:
            self.fields['farm_plot'].queryset = FarmPlot.objects.filter(farmer=farmer)

