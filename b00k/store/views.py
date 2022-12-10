from django.shortcuts import render
from .models import Book, Cart
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    # Escaparate
    return render(request, 'index.html')

def catalog(request):
    pass

@login_required
def cartView(request):
    bookOrder = request.GET.get('orderBy', 'title')
    nProducts = request.GET.get('nProducts', 25)
    pageNumber = request.GET.get('pageNumber', 1)

    
    user = request.user.get_username()
    
    cart, _ = Cart.objects.get_or_create(client=user)
    bookList = Book.objects.filter(cart__client=user).order_by(bookOrder)
    
    paginator = Paginator(bookList, nProducts)
    pageObj = paginator.get_page(pageNumber)
    totalPrice = cart.get_price()
    
    
    
    
    context = {
        'bookList': bookList,
        'pageNumber': pageNumber,
        'nProducts': nProducts,
        'pageObj': pageObj,
        'cart': cart,
        'totalPrice': totalPrice
    }
    return render(request, 'cart.html', context)