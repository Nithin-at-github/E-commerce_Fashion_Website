from django.db import models
from shop.models import *
# Create your models here.

class CartList(models.Model):
    cart_id = models.CharField(max_length=100, unique=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

class Items(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    cart = models.ForeignKey(CartList, on_delete=models.CASCADE)
    size = models.CharField(max_length=5, default='')
    quantity = models.IntegerField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.cart) +' - '+ str(self.product)

class Orders(models.Model):
    cart = models.CharField(max_length=50)
    product = models.ForeignKey(Products, on_delete=models.DO_NOTHING, default='')
    size = models.CharField(max_length=2, default='')
    amount = models.FloatField()
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
    payment_type = models.CharField(max_length=50)
    date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.firstname+' - '+str(self.date)
