from django.contrib import admin
from .models import BookAuthor, BookPublisher, BookProduct, Category, ClientProfile, Cart, Order

admin.site.register(BookAuthor)
admin.site.register(BookPublisher)
admin.site.register(BookProduct)
admin.site.register(Category)
admin.site.register(ClientProfile)
admin.site.register(Cart)
admin.site.register(Order)