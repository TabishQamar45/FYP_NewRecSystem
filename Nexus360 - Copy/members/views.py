from django.shortcuts import render
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .forms import signUpForm



# User regiser form template_View #
class UserRegiserView(generic.CreateView):
    form_class=signUpForm
    template_name='registeration/register.html'
    success_url=reverse_lazy('login')
