from django.contrib import admin
from  .models import Profile, Run_data, Event, Best_run_data, Run_notes

# Register your models here.
admin.site.register(Profile)
admin.site.register(Run_data)
admin.site.register(Event)
admin.site.register(Best_run_data)
admin.site.register(Run_notes)