from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from .forms import CreateUserForm

def index(request):
    form = CreateUserForm()
    context = {'form': form}
    if request.method == 'POST':
        print(request)
        if request.POST.get('submit') == 'register':
            form = CreateUserForm(request.POST)
            print('Hello')
            if form.is_valid():
                form.save()
        elif request.POST.get('submit') == 'login':
            username = request.POST.get('login_user')
            password = request.POST.get('login_pass')

            print(username)
            print(password)
            user = authenticate(request, username = username, password = password)
            print(user)
            if user is not None:
                messages.info(request, 'Username is correct')
            else:
                messages.info(request, 'Username is incorrect')

    return render(request, 'Astrology.html', context = context)

def book(request):
    return render(request, 'Book.html')
