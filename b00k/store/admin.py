from django.contrib import admin
from .models import Book, Category, Cart, Order

admin.site.register(Book)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(Order)