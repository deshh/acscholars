from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout



class HomePageView(TemplateView): 
    template_name = 'home.html'


class AboutPageView(TemplateView): # new 
    template_name = 'about.html'

class LogoutView(LogoutView):
    def get(self, request):
        logout(request)
        return redirect('login')
    # def user_logout(request):
    #     logout(request)
    #     return render(request, 'registration/logged_out.html', {})
    # def get(self, request):
    #     logout(request)
    #     return redirect('login')
# @login_required
# def user_logout(request):
#     logout(request)
#     return render(request, 'registration/logged_out.html', {})