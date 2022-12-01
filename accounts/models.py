from django.contrib.auth.models import User
from django.utils.timezone import now
from django.db import models
from shop.models import *

# Create your models here.

class Customers(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50, blank=True)
    email = models.CharField(max_length=50)
    mob_no = models.CharField(max_length=10)
    address_line1 = models.CharField(max_length=50)
    address_line2 = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=6)

    def __str__(self):
        return self.firstname+' '+self.lastname

class Wishlist(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user_id)+' - '+str(self.product)

class Reviews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, default='')
    email = models.CharField(max_length=50, default='')
    comment = models.TextField()
    rating = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    last_updated = models.DateTimeField(default=now)

    def __str__(self):
        return str(self.user)+' - '+str(self.product)
