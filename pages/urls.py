from django.urls import path 
from .views import HomePageView, LogoutView, AboutPageView

#  named URL of 'home'
# https://docs.djangoproject.com/en/3.1/topics/http/urls/#naming-url-patterns
urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    # https://stackoverflow.com/questions/77854460/django-logoutview-is-not-working-how-to-resolve-this-problem-using-classbased-d
    path('logout/', LogoutView.as_view(http_method_names = ['get', 'post', 'options']), name='logout'),
]