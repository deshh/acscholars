from django.urls import reverse_lazy 
from django.views import generic
from .forms import CustomUserCreationForm
from django.views.generic import TemplateView
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse

class SignupPageView(generic.CreateView): 
    form_class = CustomUserCreationForm 
    success_url = reverse_lazy('login') 
    template_name = 'registration/signup.html'

    def dispatch(self, request, *args, **kwargs):
        # Check if REGISTER_FLOW_ENABLED is False
        if not getattr(settings, 'REGISTER_FLOW_ENABLED', False):
            # Redirect to an access denied page if registration is disabled
            return redirect(reverse('access_denied'))
        return super().dispatch(request, *args, **kwargs)


class AccessDeniedView(TemplateView):
    template_name = 'access_denied.html'