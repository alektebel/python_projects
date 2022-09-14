from django.shortcuts import render

# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from labeling.models import Etiquetador, Datas
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.views.decorators.csrf import csrf_protect


def register(request):
    if request.method == 'POST':
        f = UserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            return render(request, 'accounts/login.html')

    else:
        f = UserCreationForm()
    
    return render(request, 'registration/signup.html', {'form': f})

@csrf_protect
def login(request):
    
    if request.method == 'GET':
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})
    if request.method == 'POST':
        form = AuthenticationForm(request = request, data = request.POST)

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
        # Redirect to a success page
            print('sending DATAS')
            print(Datas.objects.all())
            return render(request, 'home.html', context = {"DATAS" : Datas.objects.all()})
    else:
        # Return an 'invalid login' error message.
        return render(request, 'registration/login.html')


