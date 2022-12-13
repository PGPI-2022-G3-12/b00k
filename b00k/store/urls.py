from django.urls import path
from . import views

urlpatterns = [
    # Visualización de productos
    path('', views.index, name='index'),
    path('catalog', views.catalogAll, name='catalog'),
    path('catalog/<int:categoryId>', views.catalogCategory, name='catalog_category'),
    # Gestión de compras
    path('cart', views.cartView, name='cart'),
    path('cart/process/<int:cart_id>', views.process_cart, name='process_cart'),
    path('cart/<int:cart_id>', views.cartDetails, name='cart-details'),
    path('cart/add-from-catalog/<int:book_id>', views.add_book_from_catalog, name='add-book-from-catalog'),
    path('cart/search', views.search_cart, name='search_cart'),
    path('cart/redirect_cart_details', views.redirect_cart_details, name='cartDetails'),
    path('cart/add/<int:book_id>', views.add_book, name='cart_add'),
    path('cart/remove/<int:book_id>', views.remove_book, name='cart_remove'),
    path('cart/delete/<int:book_id>', views.delete_book_from_order, name='cart_delete'),
    # Gestión de productos
    path('<int:product_id>/', views.ProductDetailView.as_view(), name='single_product'),
    path('search/<str:q>', views.search),
    #Clientes
    path('home', views.index, name='index'),
    path('clients',views.clients, name='clients'),
    path('signup',views.signup, name='signup'),
    path('signin',views.signin, name='signin'),
    path('logout',views.ourlogout, name='logout'),
    # Información al cliente
    path('return-policy', views.return_policy, name='return-policy'),
    path('privacy', views.privacy, name='privacy'),
    path('terms-of-service', views.terms_service, name='terms-of-service'),
    path('free-delivery', views.free_delivery, name='free-delivery'),
    path('business-data', views.business_data, name='business-data'),
]