from django.shortcuts import render
from django.core.paginator import Paginator
from django.views.decorators.http import require_GET

from .models import Book, Category

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
    bookList = Book.objects.order_by(bookOrder)
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
    bookList = Book.objects.order_by(bookOrder).filter(category=categoryId)
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
