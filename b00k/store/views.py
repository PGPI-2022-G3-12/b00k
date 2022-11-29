from django.shortcuts import render

# Create your views here.

def index(request):
    # Escaparate
    return render(request, 'index.html')

def catalog(request):
    pass

def clients(request):
    return render(request,'clients.html')

def signup(request):
    return render(request,'signup.html')

def signin(request):
    return render(request,'signin.html')