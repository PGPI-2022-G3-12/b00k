from django.contrib import admin
from .models import BookProduct,BookAuthor,BookPublisher
# Register your models here.

admin.site.register(BookProduct)
admin.site.register(BookAuthor)
admin.site.register(BookPublisher)