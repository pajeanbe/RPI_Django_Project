from django.urls import path
from . import views

urlpatterns = [
    path('metrics/', views.api_metrics, name='api_metrics'),
    path('network/', views.api_network, name='api_network'),
    path('processes/', views.api_processes, name='api_processes'),
]