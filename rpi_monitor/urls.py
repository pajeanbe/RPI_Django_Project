from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/monitoring/', permanent=False)),
    path('monitoring/', include('monitoring.urls')),
    path('users/', include('users.urls')),
    path('security/', include('security.urls')),
    path('api/', include('monitoring.api_urls')),
]