from django.shortcuts import render, redirect
from .forms import *

# Create your views here.

def registration(request):
    if request.method == 'POST':
        form=RegistrationForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('index')
        
    else:
        form=RegistrationForm()
    return render(request, 'userapp/register.html', {'form':form})

def profile(request):
    return render(request, 'userapp/profile.html')

def profileupdate(request):
    if request.method=='POST':
        u_form = UpdateRegistrationForm(request.POST, instance=request.user)
        p_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('index')
    else:
        u_form = UpdateRegistrationForm(instance=request.user)
        p_form = UpdateProfileForm(instance=request.user.profile)
    context={
        'u_form':u_form,
        'p_form':p_form
    }
    return render(request, 'userapp/profileupdate.html', context)