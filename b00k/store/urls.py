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
]