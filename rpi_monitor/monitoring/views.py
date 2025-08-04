from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from .models import SystemMetrics, NetworkMetrics, ProcessInfo, NetworkInterface
from .utils import get_system_info

@login_required
def dashboard(request):
    latest_metrics = SystemMetrics.objects.first()
    network_interfaces = NetworkInterface.objects.filter(is_active=True)
    top_processes = ProcessInfo.objects.order_by('-cpu_percent')[:10]
    
    context = {
        'metrics': latest_metrics,
        'interfaces': network_interfaces,
        'processes': top_processes,
        'system_info': get_system_info(),
    }
    return render(request, 'monitoring/dashboard.html', context)

@login_required
def api_metrics(request):
    hours = int(request.GET.get('hours', 1))
    since = timezone.now() - timedelta(hours=hours)
    
    metrics = SystemMetrics.objects.filter(timestamp__gte=since).order_by('timestamp')
    
    data = {
        'timestamps': [m.timestamp.isoformat() for m in metrics],
        'cpu': [m.cpu_percent for m in metrics],
        'memory': [m.memory_percent for m in metrics],
        'disk': [m.disk_percent for m in metrics],
        'temperature': [m.temperature for m in metrics if m.temperature],
    }
    
    return JsonResponse(data)

@login_required
def api_network(request):
    hours = int(request.GET.get('hours', 1))
    since = timezone.now() - timedelta(hours=hours)
    
    interfaces = NetworkInterface.objects.filter(is_active=True)
    data = {}
    
    for interface in interfaces:
        metrics = NetworkMetrics.objects.filter(
            interface=interface,
            timestamp__gte=since
        ).order_by('timestamp')
        
        data[interface.name] = {
            'timestamps': [m.timestamp.isoformat() for m in metrics],
            'bytes_sent': [m.bytes_sent for m in metrics],
            'bytes_recv': [m.bytes_recv for m in metrics],
        }
    
    return JsonResponse(data)

@login_required
def api_processes(request):
    processes = ProcessInfo.objects.order_by('-cpu_percent')[:20]
    data = [{
        'pid': p.pid,
        'name': p.name,
        'cpu_percent': p.cpu_percent,
        'memory_percent': p.memory_percent,
        'status': p.status,
    } for p in processes]
    
    return JsonResponse({'processes': data})