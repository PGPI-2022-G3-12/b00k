from django.db import models

# Create your models here.
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
    #isbn?

    def save(self):
        return super().save()

    def change_stock(self,stock:int):
        new_stock = max(self.stock-stock,0)
        self.stock = new_stock
        self.save()

