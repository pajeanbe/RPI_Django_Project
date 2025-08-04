from django.contrib import admin
from .models import SystemMetrics, NetworkInterface, NetworkMetrics, ProcessInfo

@admin.register(SystemMetrics)
class SystemMetricsAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'cpu_percent', 'memory_percent', 'disk_percent', 'temperature']
    list_filter = ['timestamp']
    readonly_fields = ['timestamp']

@admin.register(NetworkInterface)
class NetworkInterfaceAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    list_editable = ['is_active']

@admin.register(NetworkMetrics)
class NetworkMetricsAdmin(admin.ModelAdmin):
    list_display = ['interface', 'timestamp', 'bytes_sent', 'bytes_recv']
    list_filter = ['interface', 'timestamp']

@admin.register(ProcessInfo)
class ProcessInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'pid', 'cpu_percent', 'memory_percent', 'status']
    list_filter = ['status']