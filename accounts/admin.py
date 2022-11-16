from django.contrib import admin
from .models import *

# Register your models here.

class Custmr_admin(admin.ModelAdmin):
    list_display = ['firstname', 'lastname','user_id','email']

admin.site.register(Customers, Custmr_admin)
admin.site.register(Wishlist)