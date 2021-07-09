from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm

# Create your views here.
def register(request):
    #Registration not currently supported
    #But uncommenting this and the stuff in register.html will make it work
    '''if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
        
    else:
        form = UserRegisterForm()'''
    return render(request,'users/register.html')