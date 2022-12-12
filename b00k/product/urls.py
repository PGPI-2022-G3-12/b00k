from django.urls import include, path
from . import views

urlpatterns = [
    path('<int:product_id>/', views.ProductDetailView.as_view(), name='single_product'),
    path('search/',views.ProductListView.as_view())
]