from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.index, name='index'),
    path('clients',views.clients, name='clients'),
    path('signup',views.signup, name='signup'),
    path('signin',views.signin, name='signin'),
    path('logout',views.ourlogout, name='logout')
]