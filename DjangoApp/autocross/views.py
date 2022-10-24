from datetime import date
import re
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import Event, Best_run_data, Run_data, Profile, Run_notes
from django.contrib.auth.models import User
from fuzzywuzzy import fuzz
from .forms import SignUpForm


# Create your views here.
def home(request):
    all_events = Event.objects.all().order_by('-date')#finds all events, sorts in descending order aka most recent date first       
    num_events=4
    all_data = []
    for event in all_events[:num_events]:
        runs = Best_run_data.objects.select_related('run_id__event_id').filter(run_id__event_id__event_id=event.event_id)
        pax_runs = Best_run_data.objects.select_related('run_id__event_id').filter(run_id__event_id__event_id=event.event_id).order_by('pax_diff_first')       
        all_data.append((event,runs,pax_runs)) 
    
    context = {'all_data':all_data}        
    return render(request, 'autocross/home.html', context = context)

@login_required
def user_profile(request):
    current_user = request.user
    print(current_user.id)
    current_profile = request.user.profile
    print(current_profile.id)
    
    if(request.GET.get('suggbtn')):
        current_profile.get_suggestions()

    sugg_list = current_profile.suggestion_list.split('|')
    sugg_list.pop()
    run_list = []
    for brun_id in sugg_list:
        run = Best_run_data.objects.get(b_run_id=int(brun_id))
        run_list.append(run)    
    context = {'run_list':run_list,'sugg_list':sugg_list}    
    return render(request, 'autocross/user_profile.html', context=context)

class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'autocross/signup.html'

@login_required
def analytics(request):
    return render(request,'autocross/analytics.html')
@login_required
def dashboard(request):
    return render(request,'autocross/dashboard.html')

def leaderboard(request):
    return render(request,'autocross/leaderboard.html')