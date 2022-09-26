from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy


# Create your views here.
def home(request):
    return render(request, 'autocross/home.html')

@login_required
def user_profile(request):
    return render(request, 'autocross/user_profile.html')

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'autocross/signup.html'