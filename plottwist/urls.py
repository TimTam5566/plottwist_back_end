"""
URL configuration for plottwist project.
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from users.views import CustomAuthToken  # Make sure this import is correct

def home(request):
    return HttpResponse("Welcome to Plot Twist API!")

urlpatterns = [
    path('', home),  # Root URL
    path('admin/', admin.site.urls),
    path('projects/', include('projects.urls')),  # Projects app URLs
    path('users/', include('users.urls')),        # Users app URLs
    path('api-token-auth/', CustomAuthToken.as_view(), name='api_token_auth'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


