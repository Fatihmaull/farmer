from django.urls import path
from . import views

urlpatterns = [
    path('advisories/', views.advisory_list, name='advisory_list'),
    path('advisories/<int:pk>/', views.advisory_detail, name='advisory_detail'),
    path('advisories/<int:pk>/execute/', views.advisory_execute, name='advisory_execute'),
]

