from django.urls import include, path
from . import views

urlpatterns = [
    path('products/<int:product_id>/', views.ProductDetailView.as_view()),
    path('products/search/',views.ProductListView.as_view())
]