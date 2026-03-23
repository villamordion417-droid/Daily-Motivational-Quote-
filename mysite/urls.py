"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from mysite.motivational_quotes import views as quotes_views
from mysite import views as mysite_views

urlpatterns = [
    path('health/', mysite_views.health_check, name='health_check'),
    path('', quotes_views.home, name='home'),
    # Official Django admin endpoint; make /admin/ available for admin console.
    path('admin/', admin.site.urls),
    # Keep legacy /django-admin/ working without duplicate admin namespace.
    path('django-admin/', RedirectView.as_view(url='/admin/', permanent=False)),
    # Optional legacy redirect route for staff dashboard.
    path('admin-redirect/', quotes_views.admin_redirect, name='admin_redirect'),
    path('quotes/', include('mysite.motivational_quotes.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
