from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .utils import collect_system_metrics, collect_network_metrics, collect_process_info
from .models import SystemMetrics, NetworkMetrics

@shared_task
def collect_metrics():
    collect_system_metrics()
    collect_network_metrics()
    collect_process_info()

@shared_task
def cleanup_old_metrics():
    cutoff_date = timezone.now() - timedelta(days=30)
    SystemMetrics.objects.filter(timestamp__lt=cutoff_date).delete()
    NetworkMetrics.objects.filter(timestamp__lt=cutoff_date).delete()