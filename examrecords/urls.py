from django.urls import path
from .views import (
    ExamRecordCreateView, ExamRecordUpdateView, ExamRecordDeleteView
)
from .views import filter_list_view


urlpatterns = [  
    # path('marks/', ExamRecordListView.as_view(), name='mark-list'),
    path('marks/', filter_list_view, name='marks-filter-list-view'),
    path('marks/add/', ExamRecordCreateView.as_view(), name='mark-add'),
    path('marks/<int:pk>/edit/', ExamRecordUpdateView.as_view(), name='mark-edit'),
    path('marks/<int:pk>/delete/', ExamRecordDeleteView.as_view(), name='mark-delete'),
]