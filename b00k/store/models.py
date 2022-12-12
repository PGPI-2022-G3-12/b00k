from django.db import models

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

# Gestión de compras
class Cart(models.Model):
    client = models.CharField(max_length=255, unique=True)
    books = models.ManyToManyField(BookProduct)
    
    def get_price(self):
        price = self.books.aggregate(final_price=models.Sum('price'))
        result = price["final_price"]
        if result is None:
            return 0.0
        else:
            return result
            