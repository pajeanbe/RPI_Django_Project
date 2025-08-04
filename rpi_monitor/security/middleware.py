from django.http import HttpResponseForbidden
from django.utils import timezone
from .models import IPBlacklist, SecurityEvent

class SecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check IP blacklist
        client_ip = self.get_client_ip(request)
        
        blacklisted = IPBlacklist.objects.filter(
            ip_address=client_ip,
            is_active=True
        ).filter(
            models.Q(expires_at__isnull=True) | models.Q(expires_at__gt=timezone.now())
        ).exists()
        
        if blacklisted:
            SecurityEvent.objects.create(
                event_type='suspicious_activity',
                ip_address=client_ip,
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                details={'reason': 'Blacklisted IP access attempt'}
            )
            return HttpResponseForbidden('Access denied')
        
        response = self.get_response(request)
        return response
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip