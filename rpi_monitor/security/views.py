from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from .models import SecurityEvent, IPBlacklist, IPWhitelist

def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def security_dashboard(request):
    recent_events = SecurityEvent.objects.all()[:50]
    blacklisted_ips = IPBlacklist.objects.filter(is_active=True)
    whitelisted_ips = IPWhitelist.objects.filter(is_active=True)
    
    context = {
        'events': recent_events,
        'blacklisted_ips': blacklisted_ips,
        'whitelisted_ips': whitelisted_ips,
    }
    return render(request, 'security/dashboard.html', context)