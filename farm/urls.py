from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('plots/', views.plot_list, name='plot_list'),
    path('plots/create/', views.plot_create, name='plot_create'),
    path('plots/<int:pk>/', views.plot_detail, name='plot_detail'),
    path('plots/<int:pk>/edit/', views.plot_edit, name='plot_edit'),
    path('plots/<int:pk>/delete/', views.plot_delete, name='plot_delete'),
    path('planting-records/', views.planting_record_list, name='planting_record_list'),
    path('planting-records/create/', views.planting_record_create, name='planting_record_create'),
    path('sensor-data/', views.sensor_data_list, name='sensor_data_list'),
    path('sensor-data/create/', views.sensor_data_create, name='sensor_data_create'),
    path('knowledge-base/', views.knowledge_base, name='knowledge_base'),
]

