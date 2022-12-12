from django.urls import path
from . import views

urlpatterns = [
    #Visualización de productos
    path('', views.index, name='index'),
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
    path('logout',views.ourlogout, name='logout'),
]