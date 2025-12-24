from django.urls import path
from . import views

urlpatterns = [
    path('subjects/', views.SubjectListView.as_view(), name='subject-list'),
    path('subjects/add/', views.SubjectCreateView.as_view(), name='subject-add'),
    path('subjects/<int:pk>/edit/', views.SubjectUpdateView.as_view(), name='subject-edit'),
]