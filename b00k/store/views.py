from django.shortcuts import render
from django.core.paginator import Paginator

from .models import Book, Category

# Create your views here.

def index(request):
    # Escaparate
    categoryList = Category.objects.order_by('name')
    displayCategoryList = Category.objects.order_by('name')[:6] # Order by most popular? - pending sales model

    context = {
        'categoryList': categoryList,
        'displayCategoryList': displayCategoryList,
    }

    return render(request, 'index.html', context)

def catalog(request):
    # Catálogo
    bookOrder = request.GET.get('orderBy', 'title')
    nProducts = request.GET.get('nProducts', 1)
    pageNumber = request.GET.get('page', 1)

    categoryList = Category.objects.order_by('name')
    bookList = Book.objects.order_by(bookOrder)
    paginator = Paginator(bookList, nProducts)
    pageObj = paginator.get_page(pageNumber)

    context = {
        'categoryList': categoryList,
        'bookList': pageObj,
        'pageNumber': pageNumber,
        'nProducts': nProducts,
        'pageObj': pageObj,
    }

    return render(request, 'catalog.html', context)