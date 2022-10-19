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

class Run_notes(models.Model):
    note_id = models.AutoField(primary_key=True)
    tire_pressure = models.CharField(max_length=50)
    tire_wear = models.CharField(max_length=100)
    comments = models.TextField()
    user_id = models.ForeignKey('Profile',on_delete=models.CASCADE)
    b_run_id = models.ForeignKey('Best_run_data', on_delete=models.SET_NULL,null = True)
    run_id = run_id = models.ForeignKey('Run_data', on_delete=models.SET_NULL,null = True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    car_num_list = models.TextField(blank=True)
    car_model_list = models.TextField(blank=True)
    suggestion_list = models.TextField(blank=True)
    total_cone_count = models.IntegerField(null = True)
    run_list = models.TextField(blank=True)
    events_checked_list = models.TextField(blank=True)

    
    def get_suggestions(self):
        print("hello")
        name = self.user.get_full_name()

        if self.suggestion_list == '':
            print("noData")
            all_runs = Best_run_data.objects.all()
            for run in all_runs:
                ratio = fuzz.ratio(name, run.run_id.driver_name)
                if ratio > 90:
                    self.suggestion_list+= str(run.b_run_id)+'|'
            self.save()
        else:
            print("SomeData")
            suggest_string_list = self.suggestion_list.split('|')
            suggest_string_list.pop()
            all_runs = Best_run_data.objects.all()
            for run in all_runs:
                if str(run.b_run_id) not in suggest_string_list:
                    ratio = fuzz.ratio(name, run.run_id.driver_name)
                    if ratio > 90:
                        self.suggestion_list+= str(run.b_run_id)+'|'
            self.save()
            

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
