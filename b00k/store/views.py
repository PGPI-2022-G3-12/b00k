from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .forms import ClientCreationForm, ClientLoginForm
from .models import BookProduct, Cart, Order, Category, ClientProfile
from django.core.paginator import Paginator
from django.conf import settings
from django.views.decorators.http import require_GET, require_POST
from django.views.generic import TemplateView
from django.http import Http404

BASE_URL = settings.BASE_URL

# Visualización de productos
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

@require_GET
def return_policy(request):
    return render(request, 'return-policy.html')

@require_GET
def free_delivery(request):
    return render(request, 'free-delivery.html')

@require_GET
def terms_service(request):
    return render(request, 'terms-service.html')

@require_GET
def privacy(request):
    return render(request, 'privacy.html')

@require_GET
def business_data(request):
    return render(request, 'business-data.html')

# Gestión de compras
# @login_required
def cartView(request):
    bookOrder = request.GET.get('orderBy', 'title')
    nProducts = request.GET.get('nProducts', 25)
    pageNumber = request.GET.get('page', 1)

    if request.user.is_authenticated:
        # username = request.user.username
        cart, _ = Cart.objects.get_or_create(client__user=request.user.id)
        cart.email = request.user.email
        # cart.save(force_update=True)
    else:
        cart, _ = Cart.objects.get_or_create(client__user=request.user.id)

        # cart.save(force_update=True)
    
    bookList = BookProduct.objects.filter(order__cart__id=cart.id).order_by(bookOrder)
    
    orderList = Order.objects.filter(cart=cart)
    paginator = Paginator(orderList, nProducts)
    pageObj = paginator.get_page(pageNumber)
    
    # Solo crear Orders al añadir productos al carrito
    # Solo calcular precio total si existen Orders en el carrito
    if (len(orderList) != 0):
        totalPrice = sum([order.get_cost() for order in orderList])
    else:
        totalPrice = 0

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
    bookList = BookProduct.objects.filter(order__cart__id=cart_id).order_by(bookOrder)
    
    orderList = Order.objects.get(cart=cart)
    paginator = Paginator(orderList, nProducts)
    pageObj = paginator.get_page(pageNumber)
    

    totalPrice = sum([order.get_cost() for order in orderList])
    

    cart.totalPrice = totalPrice
    cart.save()

    context = {
        'bookList': pageObj,
        'pageNumber': pageNumber,
        'nProducts': nProducts,
        'orderBy': bookOrder,
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

# Gestión de clientes
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