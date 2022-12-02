from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from fuzzywuzzy import fuzz


# Create your models here.
class Run_data(models.Model):
    run_id = models.AutoField(primary_key=True)
    class_name = models.CharField(max_length=7)
    car_num = models.IntegerField()
    driver_name = models.CharField(max_length = 36)
    car_model = models.CharField(max_length=50)
    time = models.CharField(max_length=7)
    cones_hit = models.IntegerField()
    event_id = models.ForeignKey('Event', on_delete=models.SET_NULL,null = True)

    def __str__(self):
        return f"{self.driver_name}'s time is {self.time}"

class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    date = models.DateField(unique=True)
    location = models.CharField(max_length=50)
    name = models.CharField(max_length=100)

class Best_run_data(models.Model):
    b_run_id = models.AutoField(primary_key=True)
    run_id = models.ForeignKey('Run_data', on_delete=models.SET_NULL,null = True)
    raw_class_position = models.SmallIntegerField()
    pax_class_position = models.SmallIntegerField()
    pax_time = models.CharField(max_length=7)
    note_id = models.ForeignKey('Run_notes', on_delete=models.SET_NULL,null = True)
    raw_diff_succesor = models.CharField(max_length=7)
    raw_diff_first = models.CharField(max_length=7)
    pax_diff_succesor = models.CharField(max_length=7)
    pax_diff_first = models.CharField(max_length=7)
    cones_hit_event = models.IntegerField()
    three_run_avg = models.CharField(max_length=7)

class Run_notes(models.Model):
    note_id = models.AutoField(primary_key=True)
    tire_pressure = models.CharField(max_length=50)
    tire_wear = models.CharField(max_length=100)
    comments = models.TextField()
    user_id = models.ForeignKey('Profile',on_delete=models.CASCADE)
    b_run_id = models.ForeignKey('Best_run_data', on_delete=models.SET_NULL,null = True)
    run_id = run_id = models.ForeignKey('Run_data', on_delete=models.SET_NULL,null = True)
    video_link = models.URLField(max_length=250)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    car_num_list = models.TextField(blank=True)
    car_model_list = models.TextField(blank=True)
    suggestion_list = models.TextField(blank=True)
    total_cone_count = models.IntegerField(null = True)
    run_list = models.TextField(blank=True)
    events_checked_list = models.TextField(blank=True)

    
    def get_suggestions(self):
        '''
        If suggestion list is blank, looks through all entries
        If there is some data, it will check if that id is already added
        if not, it will add the id to the list
        '''        
        name = self.user.get_full_name().lower()
        if self.suggestion_list == '':
            print("noData")            
            all_events = Event.objects.all()            
            for event in all_events:
                #adding event id to checked list
                self.events_checked_list += str(event.event_id) + '|'
                #grabbing all runs with event id 
                event_runs = Best_run_data.objects.select_related('run_id__event_id').filter(run_id__event_id__event_id=event.event_id)
                #checking each run in the event if there is a match add to suggestion list
                for run in event_runs:
                    driver_name = run.run_id.driver_name.lower()
                    ratio = fuzz.ratio(name, driver_name )                
                    if ratio > 90:
                        #print(f"name:{name}  | dname: {driver_name} | ratio:{ratio}")
                        self.suggestion_list+= str(run.b_run_id)+'|'
            #
            self.save()
        else:            
            suggest_string_list = self.suggestion_list.split('|')
            suggest_string_list.pop()
            checked_event_list = self.events_checked_list.split('|')
            checked_event_list.pop()

            all_events = Event.objects.all()
            for event in all_events:
                #if the id is not in the list we will check the event runs for matches
                if str(event.event_id) not in checked_event_list:
                    #adding id to events_checked list
                    self.events_checked_list += str(event.event_id) + '|'
                    #grabbing all runs with event id 
                    event_runs = Best_run_data.objects.select_related('run_id__event_id').filter(run_id__event_id__event_id=event.event_id)
                    #checking each run in the event if there is a match add to suggestion list
                    for run in event_runs:
                        driver_name = run.run_id.driver_name.lower()
                        if str(run.b_run_id) not in suggest_string_list:
                            ratio = fuzz.ratio(name, driver_name)
                            if ratio > 90:
                                self.suggestion_list+= str(run.b_run_id)+'|'
            #
            self.save()
    
    def add_to_run_list(self,id):
        '''
        Takes in a best run id as a str, removes it from suggestion list,
        and adds to run list if not already added.
        '''  
        local_run_list = self.run_list.split('|')
        local_run_list.pop()
        sugg_list = self.suggestion_list.split('|')
        sugg_list.pop()
        #add remove from sugglist and add to run list
        if id not in local_run_list:            
            sugg_list.remove(id)            
            self.suggestion_list = ''

            self.run_list = ''
            local_run_list.append(id)
            for sugg_id in sugg_list:
                self.suggestion_list+= (sugg_id + '|')
            for run_id in local_run_list:
                self.run_list+= (run_id + '|')
            self.save()
        else:
            #already in run list, remove from sugg list
            sugg_list.remove(id)
            self.suggestion_list = ''
            for sugg_id in sugg_list:
                self.suggestion_list+= (sugg_id + '|') 
            self.save() 

    def remove_from_run_list(self,id):
        '''
        Takes in a best run id as a str, removes form run list
        '''
        local_run_list = self.run_list.split('|')
        local_run_list.pop()
        local_run_list.remove(id)
        self.run_list = ''
        for run_id in local_run_list:
            self.run_list+= (run_id + '|')
        self.save()

    def remove_from_sugg_list(self,id):
        '''
        Takes in a best run id as a str, removes form suggestion list
        '''
        sugg_list = self.suggestion_list.split('|')
        sugg_list.pop()
        sugg_list.remove(id)
        self.suggestion_list = ''
        for sugg_id in sugg_list:
            self.suggestion_list+= (sugg_id + '|')
        self.save()
            

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
