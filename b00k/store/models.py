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
    firstName = models.CharField(max_length=150, default='Jane')
    lastName = models.CharField(max_length=150, default='Doe')
    email = models.EmailField(max_length=254, unique=True, blank=True)
    address = models.CharField(max_length=255, blank=False, null=True)
    books = models.ManyToManyField(Book)
    totalPrice = models.FloatField(default=0.0)


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
    PHYSICAL = 'physical'
    CHECKOUT = 'checkout'
    CASH = 'cash'

    DELIVERY_METHODS = ((DIGITAL, 'digital'), (PHYSICAL, 'physical'))
    PAYMENT_OPTIONS = ((CHECKOUT, 'checkout'), (CASH, 'cash'))


    delivery = models.CharField(max_length=15, choices=DELIVERY_METHODS, default=DIGITAL)
    payment = models.CharField(max_length=15, choices=PAYMENT_OPTIONS, default=CHECKOUT)

    def get_cost(self):
        return self.book.price * self.quantity
    