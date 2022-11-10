from django.db import models
# from django.template.defaulttags import slugify
from django.urls import reverse

# Create your models here.

class SubCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    desc = models.TextField(default='')
    img = models.ImageField(upload_to='subcat', default='')

    def __str__(self):
        return self.name
    
    def get_url(self):
        return reverse('scprod_list', args=[self.slug])

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    img = models.ImageField(upload_to='categ', default='')
    subcat = models.ManyToManyField(SubCategory, blank=True)

    def __str__(self):
        return self.name
    
    def get_url(self):
        return reverse('products_list', args=[self.slug])

class Offers(models.Model):
    name = models.CharField(max_length=100)
    offer = models.IntegerField()
    slug = models.SlugField(max_length=100, unique=True)
    expiry = models.DateField()

    def __str__(self):
        return self.name +' - '+ str(self.offer)+' %'
    
    def get_url(self):
        return reverse('offprod_list', args=[self.slug])

class Brands(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    logo = models.ImageField(upload_to='brands')

    def __str__(self):
        return self.name

class Products(models.Model):
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique=True)
    img = models.ImageField(upload_to='products')
    img1 = models.ImageField(upload_to='products', default='')
    img2 = models.ImageField(upload_to='products', default='')
    color = models.CharField(max_length=50, default='')
    sec_color = models.CharField(max_length=50, default='', blank=True)
    info = models.TextField(default='')
    fabric = models.CharField(max_length=50, default='')
    length = models.CharField(max_length=50, default='', blank=True)
    pattern = models.CharField(max_length=50, default='', blank=True)
    occasion = models.CharField(max_length=50, default='')
    ideal_for = models.CharField(max_length=50, default='')
    wash_care = models.CharField(max_length=50, default='')
    brand = models.ForeignKey(Brands, on_delete=models.CASCADE, default='')
    stock = models.IntegerField()
    available = models.BooleanField()
    price = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, blank=True, null=True, default='')
    featured = models.BooleanField(default=False)
    offer = models.ForeignKey(Offers, on_delete=models.CASCADE, blank=True, null=True, default='')

    def __str__(self):
        return self.name
    
    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])
    
    def actual_price(self):
        off = self.offer.offer * 0.01
        discount = self.price * off
        act_price = self.price-discount
        return int(act_price)

class Ads(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='ads')
    date = models.DateField()

    def __str__(self):
        return self.name
