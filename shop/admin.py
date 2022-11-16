from django.contrib import admin
from .models import *

# Register your models here.

class Cat_admin(admin.ModelAdmin):
    list_display = ['name','img']
    list_editable = ['img']
    prepopulated_fields = {'slug':['name']}

class Prdct_admin(admin.ModelAdmin):
    list_display = ['name', 'desc', 'price','shipping', 'stock', 'category']
    list_editable = ['price', 'shipping', 'stock', 'category']
    prepopulated_fields = {'slug':['name','desc']}

class SubCat_admin(admin.ModelAdmin):
    list_display = ['name','img']
    list_editable = ['img']
    prepopulated_fields = {'slug':['name']}

class Offr_admin(admin.ModelAdmin):
    prepopulated_fields = {'slug':['name','offer']}

class Brnd_admin(admin.ModelAdmin):
    list_display = ['name','logo']
    list_editable = ['logo']
    prepopulated_fields = {'slug':['name']}

admin.site.register(Category, Cat_admin)
admin.site.register(Products, Prdct_admin)
admin.site.register(SubCategory, SubCat_admin)
admin.site.register(Offers, Offr_admin)
admin.site.register(Brands, Brnd_admin)
admin.site.register(Ads)
