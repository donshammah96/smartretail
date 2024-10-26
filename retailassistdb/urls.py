"""
URL configuration for retailassistdb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve  # Import the serve function
from users import views as user_views
from users import (
    views as users_views,
)  # Assuming 'core' is your app name and it has views

def trigger_error(request):
    division_by_zero = 1 / 0


urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),  # Admin site
    path("core/", include("core.urls")),
    path("pos/", include("pos.urls")),
    path("users/", include("users.urls")),
    path(
        "media/<path:path>", serve, {"document_root": settings.MEDIA_ROOT}
    ),  # Serve media files
    path("", users_views.home, name="home"),  # Home view
    path("__debug__/", include("debug_toolbar.urls")),  # Debug toolbar
    path("silk/", include("silk.urls", namespace="silk")),  # Django Silk
    path("sentry-debug/", trigger_error),  # Sentry
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
