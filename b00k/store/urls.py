from django.urls import path
from . import views

urlpatterns = [
    #Visualización de productos
    path('', views.index, name='index'),
    path('return-policy', views.return_policy),
    path('privacy', views.privacy),
    path('terms-service', views.terms_service),
    path('free-delivery', views.free_delivery),
    path('business-data', views.business_data),
    path('cart', views.cartView),
    path('cart/<int:order_id>', views.cartDetails),
    path('cart/add/<int:book_id>', views.add_book),
    path('cart/remove/<int:book_id>', views.remove_book),
    path('cart/delete/<int:book_id>', views.delete_book_from_order),
    path('catalog', views.catalogAll, name='catalog'),
    path('catalog/<int:categoryId>', views.catalogCategory, name='catalog_category'),
    # Gestión de productos
    path('<int:product_id>/', views.ProductDetailView.as_view(), name='single_product'),
    path('search/<str:q>', views.ProductListView.as_view()),
    #Clientes
    path('home', views.index, name='index'),
    path('clients',views.clients, name='clients'),
    path('signup',views.signup, name='signup'),
    path('signin',views.signin, name='signin'),
    path('logout',views.ourlogout, name='logout')
]