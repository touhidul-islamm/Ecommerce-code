from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class RegistrationForm(UserCreationForm):
    class Meta:
        model= User
        fields=['first_name', 'username', 'email', 'password1', 'password2']


class UpdateRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'username', 'email']

class UpdateProfileForm(forms.ModelForm):
    date_of_birth=forms.DateField(required=False, widget=forms.DateInput(attrs={"type":"date", "class":"form-control"}))
    class Meta:
        model=Profile
        fields=['image', 'phone', 'date_of_birth']