from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from .models import Run_notes

#user sign up form
class SignUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name','last_name', 'email',  'password1','password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class']= 'form-control'
        self.fields['password1'].widget.attrs['class']= 'form-control'
        self.fields['password2'].widget.attrs['class']= 'form-control'

#form for run notes, allowing the select fields to be updated
class RunNotesForm(ModelForm):
    class Meta:
        model = Run_notes
        fields = ['tire_pressure','tire_wear','comments','video_link']