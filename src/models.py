from django.db import models


# Create your models here.

class Mobile(models.Model):
    category = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    price = models.CharField(max_length=10,blank=True,null=True)
    rating = models.CharField(max_length=3,blank=True,null=True)
    specs = models.TextField(blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    images = models.TextField(blank=True,null=True)
    reviews = models.TextField(blank=True,null=True)
    product_url = models.URLField(blank=True,null=True)

    def __str__(self):
        return self.name

class Laptop(models.Model):
    category = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    price = models.CharField(max_length=10)
    rating = models.CharField(max_length=3)
    specs = models.TextField()
    description = models.TextField()
    images = models.TextField()
    reviews = models.TextField()
    product_url = models.URLField()

    def __str__(self):
        return self.name

class TV(models.Model):
    category = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    price = models.CharField(max_length=10)
    rating = models.CharField(max_length=3)
    specs = models.TextField()
    description = models.TextField()
    images = models.TextField()
    reviews = models.TextField()
    product_url = models.URLField()

    def __str__(self):
        return self.name