from django.contrib import admin
from django.urls import path, include 
from . import views

urlpatterns = [   
    path('patrons/', views.PatronListView.as_view(), name='patron-list'),
     path('patron/add/', views.PatronCreateView.as_view(), name='patron-add'),
    path('patron/<int:pk>/edit/', views.PatronUpdateView.as_view(), name='patron-edit'),
]