from django.urls import path

from .import views

app_name="checkout"

urlpatterns = [
        path('<int:cart_id>', views.home, name='home'),
        path('<int:cart_id>/create-checkout-session/', views.create_checkout_session, name='checkout'),
        path('<int:cart_id>/success/', views.success,name='success'),
        path('<int:cart_id>/cancel/', views.cancel,name='cancel'),
]