from django.urls import path
from apps.api import views

urlpatterns = [
    path('exchange_rate/', views.exchange_rate, name='exchange_rate'),
]