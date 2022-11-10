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
        return str(self.cart)