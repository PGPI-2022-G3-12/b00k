from django.shortcuts import render

# Create your views here.

def index(request):
    # Escaparate
    return render(request, 'index.html')

def catalog(request):
    pass

def cart(request):
    return render(request, 'cart.html')