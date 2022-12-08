from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    price = models.FloatField()

class Category(models.Model):
    name = models.CharField(max_length=255)
    books = models.ManyToManyField(Book)

class Cart(models.Model):
    client = models.CharField(max_length=255, unique=True)
    books = models.ManyToManyField(Book)
    def get_price(self):
        if self.books.count == 0:
            return 0.0
        else:
            return self.books.aggregate(models.Sum('price'))