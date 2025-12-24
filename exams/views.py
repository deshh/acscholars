from django.shortcuts import render
from .models import Exam
from django.views.generic import CreateView, UpdateView, ListView
from django.urls import reverse_lazy
from .forms import ExamForm
from customaccounts.mixins import GroupRequiredMixin  # Import the mixin
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class ExamListView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    model = Exam
    template_name = 'exam_list.html'
    context_object_name = 'exams'
    paginate_by = 10
    group_required = 'operator'


# Exam Views
class ExamCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    model = Exam
    form_class = ExamForm
    template_name = 'exam_form.html'
    success_url = reverse_lazy('exam-list')  # Redirect after successful creation
    group_required = 'operator'

class ExamUpdateView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    model = Exam
    form_class = ExamForm
    template_name = 'exam_form.html'
    success_url = reverse_lazy('exam-list')  # Redirect after successful update
    group_required = 'operator'

