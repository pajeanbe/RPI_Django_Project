import psutil
import subprocess
import json
from .models import SystemMetrics, NetworkInterface, NetworkMetrics, ProcessInfo

def get_cpu_temperature():
    try:
        result = subprocess.run(['vcgencmd', 'measure_temp'], capture_output=True, text=True)
        if result.returncode == 0:
            temp_str = result.stdout.strip()
            return float(temp_str.replace('temp=', '').replace("'C", ''))
    except:
        try:
            with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
                temp = int(f.read().strip()) / 1000.0
                return temp
        except:
            pass
    return None

def collect_system_metrics():
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    load_avg = psutil.getloadavg()
    temperature = get_cpu_temperature()
    
    metrics = SystemMetrics.objects.create(
        cpu_percent=cpu_percent,
        memory_percent=memory.percent,
        memory_used=memory.used,
        memory_total=memory.total,
        disk_percent=disk.percent,
        disk_used=disk.used,
        disk_total=disk.total,
        temperature=temperature,
        load_avg_1=load_avg[0],
        load_avg_5=load_avg[1],
        load_avg_15=load_avg[2]
    )
    return metrics

def collect_network_metrics():
    net_io = psutil.net_io_counters(pernic=True)
    
    for interface_name, stats in net_io.items():
        interface, created = NetworkInterface.objects.get_or_create(name=interface_name)
        
        NetworkMetrics.objects.create(
            interface=interface,
            bytes_sent=stats.bytes_sent,
            bytes_recv=stats.bytes_recv,
            packets_sent=stats.packets_sent,
            packets_recv=stats.packets_recv
        )

def collect_process_info():
    ProcessInfo.objects.all().delete()  # Clear old data
    
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
        try:
            ProcessInfo.objects.create(
                pid=proc.info['pid'],
                name=proc.info['name'],
                cpu_percent=proc.info['cpu_percent'] or 0,
                memory_percent=proc.info['memory_percent'] or 0,
                status=proc.info['status']
            )
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

def get_system_info():
    return {
        'hostname': psutil.boot_time(),
        'platform': psutil.platform,
        'cpu_count': psutil.cpu_count(),
        'boot_time': psutil.boot_time(),
    }