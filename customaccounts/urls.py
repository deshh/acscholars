from django.urls import path 
from .views import SignupPageView, AccessDeniedView
from django.conf import settings
from . import views

urlpatterns = [
    path('signup/', SignupPageView.as_view(), name='signup'),
    path('access-denied/', AccessDeniedView.as_view(), name='access_denied'),
]

if getattr(settings, 'REGISTER_FLOW_ENABLED', False):
    urlpatterns += [
        path('signup/', views.SignupPageView.as_view(), name='signup'),
    ]