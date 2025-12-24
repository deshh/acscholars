
from django.contrib import admin
from django.urls import path, include 
from . import views

urlpatterns = [
path('students/', views.StudentListView.as_view(), name='student-list'),
    path('students/<int:pk>/', views.StudentDetailView.as_view(), name='student-detail'),
    path('students/<int:pk>/marks/', views.StudentMarksView.as_view(), name='student-marks'),
    path('students/add/', views.StudentCreateView.as_view(), name='student-add'),
    path('students/<int:pk>/edit/', views.StudentUpdateView.as_view(), name='student-edit'),
    # path('student/<int:student_id>/marks-chart/', views.student_marks_chart, name='student-marks-chart'),
    path('students/<int:pk>/marks-chart/', views.StudentMarksChartView.as_view(), name='student-marks-chart'),
    path('students/<int:pk>/delete/', views.StudentDeleteView.as_view(), name='student-delete'),
]