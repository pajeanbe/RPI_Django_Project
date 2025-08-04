from django.db import models
from django.utils import timezone

class SystemMetrics(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    cpu_percent = models.FloatField()
    memory_percent = models.FloatField()
    memory_used = models.BigIntegerField()
    memory_total = models.BigIntegerField()
    disk_percent = models.FloatField()
    disk_used = models.BigIntegerField()
    disk_total = models.BigIntegerField()
    temperature = models.FloatField(null=True, blank=True)
    load_avg_1 = models.FloatField()
    load_avg_5 = models.FloatField()
    load_avg_15 = models.FloatField()

    class Meta:
        ordering = ['-timestamp']

class NetworkInterface(models.Model):
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class NetworkMetrics(models.Model):
    interface = models.ForeignKey(NetworkInterface, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    bytes_sent = models.BigIntegerField()
    bytes_recv = models.BigIntegerField()
    packets_sent = models.BigIntegerField()
    packets_recv = models.BigIntegerField()
    
    class Meta:
        ordering = ['-timestamp']

class ProcessInfo(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    pid = models.IntegerField()
    name = models.CharField(max_length=255)
    cpu_percent = models.FloatField()
    memory_percent = models.FloatField()
    status = models.CharField(max_length=50)
    
    class Meta:
        ordering = ['-cpu_percent']