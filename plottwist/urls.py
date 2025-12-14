"""
============================================================
MAIN URL CONFIGURATION - The Master Address Book
============================================================
This is the FIRST place Django looks when a request comes in.
It routes requests to the appropriate app.
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from users.views import CustomAuthToken  # Make sure this import is correct

def home(request):
    """Simple homepage - just returns a welcome message"""
    return HttpResponse("Welcome to Plot Twist API!")

urlpatterns = [
    # ============================================================
    # ROOT URL
    # ============================================================
    path('', home),
    # GET / → "Welcome to Plot Twist API!"
    
    # ============================================================
    # ADMIN PANEL
    # ============================================================
    path('admin/', admin.site.urls),
    # GET /admin/ → Django's built-in admin interface
    # You can manage users, projects, pledges here
    
    # ============================================================
    # APP URLS - Delegate to each app's urls.py
    # ============================================================
    path('projects/', include('projects.urls')),
    # /projects/...  → Handled by projects/urls.py
    # This is why /projects/ shows all projects
    # And /projects/1/ shows project #1
    path('users/', include('users.urls')),
    # /users/... → Handled by users/urls.py
    
    # ============================================================
    # AUTHENTICATION
    # ============================================================      
    path('api-token-auth/', CustomAuthToken.as_view(), name='api_token_auth'),
    # POST /api-token-auth/ → Login endpoint
    # Send: {"username": "tim", "password": "secret"}
    # Get:  {"token": "abc123", "user_id": 1, "email": "tim@email.com"}
]

# ============================================================
# SERVE MEDIA FILES IN DEVELOPMENT
# ============================================================
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
"""
In development (DEBUG=True), Django will serve uploaded media files.
In production, Cloudinary handles this instead.
"""

