from django.shortcuts import render, redirect
from .models import Book, Cart, Order
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    # Escaparate
    return render(request, 'index.html')

def catalog(request):
    pass

def return_policy(request):
    return render(request, 'return-policy.html')

def free_delivery(request):
    return render(request, 'free-delivery.html')

def terms_service(request):
    return render(request, 'terms-service.html')

def privacy(request):
    return render(request, 'privacy.html')

def business_data(request):
    return render(request, 'business-data.html')


# @login_required
def cartView(request):
    bookOrder = request.GET.get('orderBy', 'title')
    nProducts = request.GET.get('nProducts', 25)
    pageNumber = request.GET.get('pageNumber', 1)

    placeholder = ''

    if request.user.is_authenticated:
        username = request.user.username
        cart, _ = Cart.objects.get_or_create(client=username)

        cart.firstName = request.user.first_name
        cart.lastName = request.user.last_name
        cart.email = request.user.email
        
        cart.save()
    else:
        username = placeholder

        cart, _ = Cart.objects.get_or_create(client=placeholder)
        cart.firstName = placeholder
        cart.lastName = placeholder
        cart.email = placeholder
        cart.save()


    
    
    bookList = Book.objects.filter(order__cart__id=cart.id).order_by(bookOrder)
    
    orderList = Order.objects.get_or_create(cart=cart)
    paginator = Paginator(orderList, nProducts)
    pageObj = paginator.get_page(pageNumber)
    

    totalPrice = sum([order.get_cost() for order in orderList])
    

    cart.totalPrice = totalPrice
    cart.save()



    context = {
        'bookList': bookList,
        'pageNumber': pageNumber,
        'nProducts': nProducts,
        'pageObj': pageObj,
        'cart': cart,
        'totalPrice': totalPrice,
        'orderList': orderList

    }
    return render(request, 'cart.html', context)

def cartDetails(request, cart_id):
    bookOrder = request.GET.get('orderBy', 'title')
    nProducts = request.GET.get('nProducts', 25)
    pageNumber = request.GET.get('pageNumber', 1)

    cart = Cart.objects.get(id=cart_id)
    # if request.user.is_authenticated:
    #     username = request.user.username
    #     cart, _ = Cart.objects.get_or_create(client=username)

    #     cart.firstName = request.user.first_name
    #     cart.lastName = request.user.last_name
    #     cart.email = request.user.email
        
    #     cart.save()
    # else:
    #     username = placeholder

    #     cart, _ = Cart.objects.get_or_create(client=placeholder)
    #     cart.firstName = placeholder
    #     cart.lastName = placeholder
    #     cart.email = placeholder
    #     cart.save()


    
    
    bookList = Book.objects.filter(order__cart__id=cart_id).order_by(bookOrder)
    
    orderList = Order.objects.get_or_create(cart=cart)
    paginator = Paginator(orderList, nProducts)
    pageObj = paginator.get_page(pageNumber)
    

    totalPrice = sum([order.get_cost() for order in orderList])
    

    cart.totalPrice = totalPrice
    cart.save()

    context = {
        'bookList': bookList,
        'pageNumber': pageNumber,
        'nProducts': nProducts,
        'pageObj': pageObj,
        'cart': cart,
        'totalPrice': totalPrice,
        'orderList': orderList

    }
    return render(request, 'order-details.html', context)


def add_book(request, book_id):
    order_id = request.GET['order_id']
    order = Order.objects.get(id=order_id)

    total_amount = int(request.GET['quantity'] + order.quantity)
    
    order.quantity = total_amount
    
    order.save()
    return redirect(request.GET['division'])

def remove_book(request, book_id):
    order_id = request.GET['order_id']
    order = Order.objects.get(id=order_id)

    total_amount = int(order.quantity - request.GET['quantity'])
    
    order.quantity = total_amount
    
    order.save()
    return redirect(request.GET['division'])


def delete_book_from_order(request, book_id):
    order_id = request.GET['order_id']
    order = Order.objects.get(id=order_id)

    order.delete()
    return redirect(request.GET['division'])