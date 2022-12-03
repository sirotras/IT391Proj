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
from json import dumps


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
    #print(current_user.id)
    current_profile = request.user.profile
    #print(current_profile.id)
    
    #update suggestions
    if(request.GET.get('suggbtn')):
        current_profile.get_suggestions()

    #adding run to run list
    if(request.GET.get('sugg_add')):
        current_profile.add_to_run_list(request.GET['sugg_add'])
    #Removing run from suggestion list
    if(request.GET.get('sugg_rem')):
        print(request.GET['sugg_rem'])
        current_profile.remove_from_sugg_list(request.GET['sugg_rem'])
    #Removing run from run list
    if(request.GET.get('run_rem')):
        current_profile.remove_from_run_list(request.GET['run_rem'])
    #Rests the suggestion list
    if(request.GET.get('sugg_reset')):
        current_profile.suggestion_list = ''
        current_profile.events_checked_list = ''
        current_profile.save()
    #Resets the runs list
    if(request.GET.get('run_reset')):
        current_profile.remove_all_run_notes()
        current_profile.run_list = ''
        current_profile.save()

    current_profile.count_cones()
    
    sugg_list = current_profile.suggestion_list.split('|')
    sugg_list.pop()
    events_checked = current_profile.events_checked_list.split('|')
    events_checked.pop()
    local_run_list = current_profile.run_list.split('|')
    local_run_list.pop()
    #will hold the runs based of best run id brun
    sugg_run_list =[]    
    run_note_list = []
    for brun_id in sugg_list:
        run = Best_run_data.objects.get(b_run_id=int(brun_id))
        sugg_run_list.append(run)
    for brun_id in local_run_list:
        run = Best_run_data.objects.get(b_run_id=int(brun_id))
        note = Run_notes.objects.get(b_run_id = Best_run_data.objects.get(b_run_id = int(brun_id)))
        run_note_list.append((run,note))

    context = {'sugg_run_list':sugg_run_list,'sugg_list':sugg_list, 'run_note_list':run_note_list,'events_checked':events_checked}    
    return render(request, 'autocross/user_profile.html', context=context)

class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'autocross/signup.html'

@login_required
def analytics(request):
    #get profile of the current logged in user
    current_profile = request.user.profile
    #Gets suggestion list without the pipe as a list
    #holds the best run id
    local_run_list = current_profile.run_list.split('|')
    local_run_list.pop()
    run_run_list = []
    coordinates1 = ["Run Date" , "Difference From First (Raw)"]
    coordinates2 = ["Run Date" , "Difference From First (PAX)"] 
    #gets the best run data for each best run id
    for brun_id in local_run_list:
        run = Best_run_data.objects.get(b_run_id=int(brun_id))
        run_run_list.append(run)
        
    #sorting run list oldest events first
    run_run_list.sort(key=lambda x: x.run_id.event_id.date)
    #adding raw and pax data to coordinates1 & 2
    for run in run_run_list:
        if run.raw_diff_first != "":
            coordinates1.append(str(run.run_id.event_id.date))
            coordinates1.append(str(run.raw_diff_first))
        if run.pax_diff_first != "":
            coordinates2.append(str(run.run_id.event_id.date))
            coordinates2.append(str(run.pax_diff_first)) 
    dataJSON1 = dumps(coordinates1)        
    dataJSON2 = dumps(coordinates2)
    
    context = {'run_list':run_run_list,'sugg_list':run_run_list, 'data1':dataJSON1, 'data2':dataJSON2 , 'cones':current_profile.total_cone_count}
    return render(request,'autocross/analytics.html', context=context)

@login_required
def dashboard(request):
    return render(request,'autocross/dashboard.html')

def leaderboard(request):
    return render(request,'autocross/leaderboard.html')

def all_events(request):
    years = ['2022','2021','2020']
    all_data = {'2022':'2022 Data', '2021':'2021 Data', '2020':'2020 Data'}
    year_data = ""
    year_data = []
    if(request.GET.get('year_btn')):        
        year = request.GET['year_btn']
        #check to see if the keys exists, if not it will still show no data
        if year in all_data:
            #gets all events by year and sorts by most recent
            yearly_events = Event.objects.all().filter(date__year=int(year)).order_by('-date')
            for event in yearly_events:
                runs = Best_run_data.objects.select_related('run_id__event_id').filter(run_id__event_id__event_id=event.event_id)
                year_data.append((event, runs))
                all_data[year]=year_data

            
        
    
    context = {'years':years,'year_data':year_data}
    return render(request, 'autocross/all_events.html', context = context)
