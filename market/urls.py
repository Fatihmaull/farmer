from django.urls import path
from . import views

urlpatterns = [
    path('market-prices/', views.market_price_list, name='market_price_list'),
]

