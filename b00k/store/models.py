from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    price = models.FloatField()

class Category(models.Model):
    name = models.CharField(max_length=255)
    books = models.ManyToManyField(Book)

class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) #Aqui iría todo lo importante
    address = models.CharField(max_length=255)

    def __str__(self):
        return "({fName} {lName}, {uName})".format(fname=self.user.first_name,lName =self.user.last_name, uName= self.user.username)
    

