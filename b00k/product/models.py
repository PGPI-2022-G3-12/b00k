from django.db import models

# Create your models here.
class BookAuthor(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

class BookPublisher(models.Model):
    name = models.CharField(max_length=15)

class BookProduct(models.Model):
    title = models.CharField(max_length=30)
    author = models.ForeignKey(BookAuthor,on_delete=models.CASCADE)
    editorial = models.ForeignKey(BookPublisher,on_delete=models.CASCADE)
    description = models.CharField(max_length=200,null=True)
    price = models.DecimalField(max_digits=4,decimal_places=2)
    picture = models.ImageField()
    #isbn?
