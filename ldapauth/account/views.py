from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse


@login_required(login_url="/account/login/")
def home(request):
    return HttpResponse('hi')

def user_login(request):
    if request.method == "POST":
        # check
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)   
        if user is not None:
            auth.login(request, user) 
            return redirect('home')
        else:
            messages.add_message(request, messages.WARNING, 'username or password is invalid')

    return render(request, 'account/login.html')

def user_logout(request):
    auth.logout(request)
    return redirect('login')