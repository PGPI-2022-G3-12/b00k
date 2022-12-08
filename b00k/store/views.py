from django.shortcuts import render
from .models import Book, Cart
from django.core.paginator import Paginator
# Create your views here.

def index(request):
    # Escaparate
    return render(request, 'index.html')

def catalog(request):
    pass

def cartView(request):
    bookOrder = request.GET.get('orderBy', 'title')
    nProducts = request.GET.get('nProducts', 25)
    pageNumber = request.GET.get('pageNumber', 1)

    #comprueba que haya iniciado sesion
    if request.user.is_authenticated:
        user = request.user.get_username()
        
        
        cart, _ = Cart.objects.get_or_create(client=user)
        bookList = Book.objects.filter(cart__client=user).order_by(bookOrder)

        paginator = Paginator(bookList, nProducts)
        pageObj = paginator.get_page(pageNumber)
        totalPrice = cart.get_price()
        
        
        
        context = {
            'bookList': pageObj,
            'pageNumber': pageNumber,
            'nProducts': nProducts,
            'pageObj': pageObj,
            'cart': cart,
            'totalPrice': totalPrice
        }
        return render(request, 'cart.html', context)

        
    
    else:
        return render(request, 'index.html')