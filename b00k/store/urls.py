from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('return-policy', views.return_policy),
    path('privacy', views.privacy),
    path('terms-service', views.terms_service),
    path('free-delivery', views.free_delivery),
    path('business-data', views.business_data),
    path('cart', views.cartView),
    path('cart/add/<int:book_id>', views.add_book),
    path('cart/remove/<int:book_id>', views.remove_book),
    path('cart/delete/<int:book_id>', views.delete_book_from_order)
]