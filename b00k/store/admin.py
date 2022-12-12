from django.contrib import admin
from .models import BookProduct, BookAuthor, BookPublisher, Category, Cart

admin.site.register(BookProduct)
admin.site.register(BookAuthor)
admin.site.register(BookPublisher)
admin.site.register(Category)
admin.site.register(Cart)