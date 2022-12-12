from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('catalog', views.catalogAll, name='catalog'),
    path('catalog/<int:categoryId>', views.catalogCategory, name='catalog_category')
]