"""
URL configuration for config project.

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
from customaccounts import views

urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),
    # User management
    path('accounts/', include('django.contrib.auth.urls')), # new
    # Local apps
    path('accounts/', include('customaccounts.urls')),
    path('', include('pages.urls')),
    path('students/', include('students.urls')),
    path('marks/', include('examrecords.urls')),
    path('exams/', include('exams.urls')),
    path('subjects/', include('subjects.urls')),
    path('patrons/', include('patrons.urls')),
]

if getattr(settings, 'REGISTER_FLOW_ENABLED', False):
    urlpatterns += [
        path('signup/', views.SignupPageView.as_view(), name='signup'),
    ]