from django.shortcuts import render
from .models import Subject
from django.views.generic import CreateView, UpdateView, ListView
from django.urls import reverse_lazy
from .forms import SubjectForm
from customaccounts.mixins import GroupRequiredMixin  # Import the mixin
from django.contrib.auth.mixins import LoginRequiredMixin

# Subject Views
class SubjectListView(GroupRequiredMixin, ListView):
    model = Subject
    template_name = 'subject_list.html'
    context_object_name = 'subjects'
    paginate_by = 10
    group_required = 'operator'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # Ensure this line is present
        # Add additional context if needed

        is_operator = False
        if self.request.user.is_authenticated:
            is_operator = self.request.user.groups.filter(name='operator').exists()

        context['is_operator'] = is_operator
        return context

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     return queryset.order_by('id')


class SubjectCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'subject_form.html'
    success_url = reverse_lazy('subject-list')  # Redirect after successful creation
    group_required = 'operator'

class SubjectUpdateView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'subject_form.html'
    success_url = reverse_lazy('subject-list')  # Redirect after successful update
    group_required = 'operator'