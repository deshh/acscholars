from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView
from .models import Patron
from .forms import PatronForm
from customaccounts.mixins import GroupRequiredMixin  # Import the mixin
from django.contrib.auth.mixins import LoginRequiredMixin

class PatronListView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    model = Patron
    template_name = 'patron_list.html'
    context_object_name = 'patrons'
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

class PatronCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    model = Patron
    form_class = PatronForm
    template_name = 'patron_form.html'
    success_url = reverse_lazy('patron-list')  # Adjust to your actual patron list view URL
    group_required = 'operator'

class PatronUpdateView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    model = Patron
    form_class = PatronForm
    template_name = 'patron_form.html'
    success_url = reverse_lazy('patron-list')
    group_required = 'operator'

    def form_invalid(self, form):
        print(form.errors)  # or log the errors
        return super().form_invalid(form)
    
    def form_valid(self, form):
        # Avoid unique constraint violation
        if form.instance.pk:
            if Patron.objects.exclude(pk=form.instance.pk).filter(email=form.cleaned_data['email']).exists():
                form.add_error('email', 'A patron with this email already exists.')
                return self.form_invalid(form)
        return super().form_valid(form)
