from math import frexp
from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(CartList)
admin.site.register(Items)
admin.site.register(Orders)