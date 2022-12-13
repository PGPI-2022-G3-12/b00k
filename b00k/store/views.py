from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .forms import ClientCreationForm, ClientLoginForm
from django.views.decorators.csrf import csrf_exempt
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
        clientP = ClientProfile.objects.get(user=request.user)
        cart, _ = Cart.objects.get_or_create(client__user=request.user)
        
        cart.email = request.user.email
        cart.client = clientP
        # cart.save(force_update=True)
    else:
        cart, _ = Cart.objects.get_or_create(client__user__id=request.user.id)

        # cart.save(force_update=True)
    
    bookList = BookProduct.objects.filter(order__cart=cart.id).order_by(bookOrder)
    
    orderList = Order.objects.filter(cart__id=cart.id)
    paginator = Paginator(orderList, nProducts)
    pageObj = paginator.get_page(pageNumber)
    
    # Solo crear Orders al añadir productos al carrito
    # Solo calcular precio total si existen Orders en el carrito
    if (len(orderList) != 0):
        totalPrice = sum([order.get_cost() for order in orderList])
    else:
        totalPrice = 0

    cart.totalPrice = totalPrice

    showPayButton = cart.delivery_state == "Pendiente de pago"

    cart.save(force_update=True)

    context = {
        'bookList': bookList,
        'pageNumber': pageNumber,
        'nProducts': nProducts,
        'pageObj': pageObj,
        'cart': cart,
        'cartId': cart.id,
        'showPayButton': showPayButton,
        'totalPrice': totalPrice,
        'orderList': orderList
    }

    return render(request, 'cart.html', context)

def process_cart(request, cart_id):
    cart_string_id = str(cart_id)
    return redirect("/checkout/"+cart_string_id)

def search_cart(request):
    return render(request, 'search.html')

@csrf_exempt
def redirect_cart_details(request):

    details_id = request.GET['cart_id']
    return redirect("/store/cart/"+details_id)

def cartDetails(request, cart_id):
    bookOrder = request.GET.get('orderBy', 'title')
    nProducts = request.GET.get('nProducts', 25)
    pageNumber = request.GET.get('pageNumber', 1)

    cart = Cart.objects.get(id=cart_id)
    bookList = BookProduct.objects.filter(order__cart__id=cart_id).order_by(bookOrder)
    
    orderList = Order.objects.filter(cart=cart.id)
    paginator = Paginator(orderList, nProducts)
    pageObj = paginator.get_page(pageNumber)
    
    showPayButton = cart.delivery_state == "Pendiente de pago"

    if (len(orderList) != 0):
        totalPrice = sum([order.get_cost() for order in orderList])
    else:
        totalPrice = 0

    cart.totalPrice = totalPrice

    cart.save()

    context = {
        'bookList': pageObj,
        'pageNumber': pageNumber,
        'nProducts': nProducts,
        'orderBy': bookOrder,
        'pageObj': pageObj,
        'cart': cart,
        'showPayButton': showPayButton,
        'totalPrice': totalPrice,
        'orderList': orderList
    }

    return render(request, 'order-details.html', context)

def add_book_from_catalog(request, book_id):
    if request.user.is_authenticated:
        clientP = ClientProfile.objects.get(user=request.user)
        cart, _ = Cart.objects.get_or_create(client__user=request.user.id)
        cart.client = clientP
        cart.email = request.user.email
    else:
        cart, _ = Cart.objects.get_or_create(client__user=request.user.id)

    order, _ = Order.objects.get_or_create(cart=cart, book_id=book_id)
    

    book_id_string = str(book_id)
    order_id_string = str(order.id)
    contenido_get = '?order_id=' + order_id_string
    string_to_add = '&'
    for k,v in request.GET.items():
        contenido_get += string_to_add + k + "=" + str(v)
    return redirect("/store/cart/add/" + book_id_string + contenido_get)


def add_book(request, book_id):
    order_id = request.GET['order_id']
    order = Order.objects.get(id=order_id)

    total_amount = int(request.GET['quantity']) + order.quantity
    
    order.quantity = total_amount
    
    order.save()
    return redirect(request.GET['division'])

def remove_book(request, book_id):
    order_id = request.GET['order_id']
    order = Order.objects.get(id=order_id)

    total_amount = order.quantity - int(request.GET['quantity'])
    
    order.quantity = total_amount
    
    order.save()
    return redirect(request.GET['division'])


def delete_book_from_order(request, book_id):
    order_id = request.GET['order_id']
    order = Order.objects.get(id=order_id)

    order.delete()
    return redirect(request.GET['division'])

# Gestion de productos

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