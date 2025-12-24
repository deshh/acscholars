from django.contrib import admin
from django.urls import path, include 
from . import views

urlpatterns = [   
    path('exams/', views.ExamListView.as_view(), name='exam-list'),
    path('exams/add/', views.ExamCreateView.as_view(), name='exam-add'),
    path('exams/<int:pk>/edit/', views.ExamUpdateView.as_view(), name='exam-edit'),
]