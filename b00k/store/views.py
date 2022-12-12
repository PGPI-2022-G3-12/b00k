from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .forms import ClientCreationForm, ClientLoginForm
from .models import ClientProfile
# Create your views here.

def index(request):
    # Escaparate
    return render(request, 'index.html')

def catalog(request):
    pass

def clients(request):
    return render(request,'clients.html')

def signup(request):
    if request.method == "POST":
        form = ClientCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            address = form.cleaned_data.get('address')
            user = authenticate(request=request,username=username, password=password)
            client = ClientProfile(user=user,address=address)
            client.save()
            login(request, user)
            return redirect('index')
        return render(request,'signup.html', {'form':form})
    else:
        form = ClientCreationForm()
    return render(request,'signup.html', {'form':form})

def signin(request):
    if request.method == "POST":
        form = ClientLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
        else:
            print("error")
        return render(request,'signin.html', {'form':form})
        
    else:
        form = ClientLoginForm()
    return render(request,'signin.html', {'form':form})

def ourlogout(request):
    logout(request)
    return redirect('index')