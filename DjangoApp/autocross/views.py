from datetime import date
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import Event, Best_run_data, Run_data


# Create your views here.
def home(request):
    all_events = Event.objects.all().order_by('-date')#finds all events, sorts in descending order aka most recent date first       
    num_events=4
    all_data = []
    for event in all_events[:num_events]:
        runs = Best_run_data.objects.select_related('run_id__event_id').filter(run_id__event_id__event_id=event.event_id)        
        all_data.append((event,runs)) 
    
    context = {'all_data':all_data}        
    return render(request, 'autocross/home.html', context = context)

@login_required
def user_profile(request):
    return render(request, 'autocross/user_profile.html')

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'autocross/signup.html'