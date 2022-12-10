from django.urls import include, path
from . import views

urlpatterns = [
    path('<int:product_id>/', views.ProductDetailView.as_view()),
    path('search/',views.ProductListView.as_view())
]