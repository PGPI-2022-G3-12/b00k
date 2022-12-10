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
    
    # def get_price(self):
    #     price = self.books.aggregate(final_price=models.Sum('price'))
    #     result = price["final_price"]
    #     if result is None:
    #         return 0.0
    #     else:
    #         return result
class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    DIGITAL = 'digital'
    FISICO = 'fisico'

    DELIVERY_METHODS = ((DIGITAL, 'digital'), (FISICO, 'fisico'))

    delivery = models.CharField(max_length=15, choices=DELIVERY_METHODS, default=DIGITAL)

    def get_cost(self):
        return self.book.price * self.quantity
    