from django.db import models
from django.contrib.auth.models import User

class BookAuthor(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def save(self):
        return super().save()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class BookPublisher(models.Model):
    name = models.CharField(max_length=15)

    def save(self):
        return super().save()

    def __str__(self):
        return self.name

class BookProduct(models.Model):
    title = models.CharField(max_length=30)
    author = models.ForeignKey(BookAuthor,on_delete=models.CASCADE)
    editorial = models.ForeignKey(BookPublisher,on_delete=models.CASCADE)
    description = models.CharField(max_length=200,null=True)
    price = models.DecimalField(max_digits=4,decimal_places=2)
    picture = models.ImageField(upload_to="media")
    stock = models.IntegerField(default=0)

    def save(self):
        return super().save()

    def change_stock(self,stock:int):
        new_stock = max(self.stock-stock,0)
        self.stock = new_stock
        self.save()

class Category(models.Model):
    name = models.CharField(max_length=255)
    books = models.ManyToManyField(BookProduct)

class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) #Aqui iría todo lo importante
    address = models.CharField(max_length=255)

    def __str__(self):
        return "({fName} {lName}, {uName})".format(fName=self.user.first_name,lName =self.user.last_name, uName= self.user.username)

class Cart(models.Model):
    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, blank=True, null=True)
    email = models.EmailField(max_length=254, null=True)
    books = models.ManyToManyField(BookProduct)
    totalPrice = models.DecimalField(max_digits=4,decimal_places=2, default=0.0)

    CHECKOUT = 'checkout'
    CASH = 'cash'

    PAYMENT_OPTIONS = ((CHECKOUT, 'checkout'), (CASH, 'cash'))

    DELIVERED = 'Entregado'
    EN_ROUTE = 'En Camino'
    PROCESSING = 'En Proceso'
    PENDING_PAYMENT = 'Pendiente de pago'

    DIGITAL = 'Digital'
    PHYSICAL = 'Físico'
    CHECKOUT = 'Pasarela de Pago'
    CASH = 'En Efectivo'

    DELIVERY_METHODS = ((DIGITAL, 'Digital'), (PHYSICAL, 'Fisico'))
    PAYMENT_OPTIONS = ((CHECKOUT, 'Pasarela de Pago'), (CASH, 'En Efectivo'))
    DELIVERY_STATE = ((DELIVERED, 'Entregado'), (EN_ROUTE,'En Camino'), (PROCESSING,'En Proceso'), (PENDING_PAYMENT, 'Pendiente de Pago'))

    delivery = models.CharField(max_length=20, choices=DELIVERY_METHODS, default=DIGITAL)
    payment = models.CharField(max_length=20, choices=PAYMENT_OPTIONS, default=CHECKOUT)
    delivery_state = models.CharField(max_length=20, choices=DELIVERY_STATE, default=PENDING_PAYMENT)

class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    book = models.ForeignKey(BookProduct, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    def get_cost(self):
        return self.book.price * self.quantity