from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .forms import ClientCreationForm, ClientLoginForm
# Create your views here.
from django.conf import settings
from django.core.paginator import Paginator
from django.views.decorators.http import require_GET, require_POST
from django.views.generic import TemplateView
from django.http import Http404

from .models import BookProduct, Category, ClientProfile

BASE_URL = settings.BASE_URL

# 
@require_GET
def index(request):
    # Escaparate
    categoryList = Category.objects.order_by('name')
    displayCategoryList = Category.objects.order_by('name')[:6] # Order by most popular? - pending sales model

    context = {
        'categoryList': categoryList,
        'displayCategoryList': displayCategoryList,
    }

    return render(request, 'index.html', context)

@require_GET
def catalogAll(request):
    # Catálogo - Todas las categorías
    bookOrder = request.GET.get('sortBy', 'title')
    nProducts = request.GET.get('nProducts', 25)
    pageNumber = request.GET.get('page', 1)

    categoryList = Category.objects.order_by('name')
    bookList = BookProduct.objects.order_by(bookOrder)
    paginator = Paginator(bookList, nProducts)
    pageObj = paginator.get_page(pageNumber)

    context = {
        'categoryList': categoryList,
        'bookList': pageObj,
        'pageNumber': pageNumber,
        'nProducts': nProducts,
        'orderBy': bookOrder,
        'pageObj': pageObj,
        'categoryId': None,
    }

    return render(request, 'catalog.html', context)

@require_GET
def catalogCategory(request, categoryId):
    # Catálogo
    bookOrder = request.GET.get('orderBy', 'title')
    nProducts = request.GET.get('nProducts', 25)
    pageNumber = request.GET.get('page', 1)

    categoryList = Category.objects.order_by('name')
    bookList = BookProduct.objects.order_by(bookOrder).filter(category=categoryId)
    paginator = Paginator(bookList, nProducts)
    pageObj = paginator.get_page(pageNumber)

    context = {
        'categoryList': categoryList,
        'bookList': pageObj,
        'pageNumber': pageNumber,
        'nProducts': nProducts,
        'orderBy': bookOrder,
        'pageObj': pageObj,
        'categoryId': categoryId,
    }

    return render(request, 'catalog.html', context)

# Gestion de productos
class ProductListView(TemplateView):
    template_name = 'list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query:str = kwargs.get('q','')
        try:
            products = BookProduct.objects.filter(title__contains=query)
            context['products'] = products
            context['query'] = query

        except:
            raise Http404
        return context

@require_GET
def search(request,q):
    bookOrder = request.GET.get('sortBy', 'title')
    nProducts = request.GET.get('nProducts', 25)
    pageNumber = request.GET.get('page', 1)

    categoryList = Category.objects.order_by('name')
    bookList = BookProduct.objects.filter(title__contains=q).order_by(bookOrder)
    paginator = Paginator(bookList, nProducts)
    pageObj = paginator.get_page(pageNumber)

    context = {
        'categoryList': categoryList,
        'bookList': pageObj,
        'pageNumber': pageNumber,
        'nProducts': nProducts,
        'orderBy': bookOrder,
        'pageObj': pageObj,
        'categoryId': None,
    }

    return render(request, 'catalog.html', context)
class ProductDetailView(TemplateView):
    template_name = 'single.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pid = kwargs.get('product_id',0)
        try:
            #TOFIX: No detecta el objeto pese a existir en la db
            product = BookProduct.objects.get(pk=pid)
            context['product'] = product
            context['BASE_URL'] = BASE_URL
        except:
            raise Http404
        return context

@require_GET
def clients(request):
    return render(request,'clients.html')

# @require_POST
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

# @require_POST
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

# @require_POST
def ourlogout(request):
    logout(request)
    return redirect('index')

