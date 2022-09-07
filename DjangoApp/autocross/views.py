from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'autocross/home.html')

def user_profile(request):
    return render(request, 'autocross/user_profile.html')