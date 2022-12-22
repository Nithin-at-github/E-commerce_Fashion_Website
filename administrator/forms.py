from django import forms
from django.contrib.auth.models import User
from django.forms import Field
from shop.models import *
from crispy_forms.helper import FormHelper, Layout

class SubCatForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ['name', 'desc', 'img']

class CatForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'img']

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brands
        fields = ['name', 'logo']

class OfferForm(forms.ModelForm):
    class Meta:
        model = Offers
        fields = ['name', 'offer', 'expiry']

class AdForm(forms.ModelForm):
    class Meta:
        model = Ads
        fields = ['name', 'img', 'date']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['name', 'desc', 'img', 'img1', 'img2', 'color', 'sec_color', 'info', 'fabric', 'length', 'pattern', 'occasion', 'ideal_for', 'wash_care', 'brand', 'stock_xs', 'stock_s', 'stock_m', 'stock_l', 'stock_xl', 'price', 'shipping', 'category', 'sub_category', 'featured', 'offer']

        def __init__(self, *args, **kwargs):
            super(ProductForm, self).__init__(*args, **kwargs)
            self.helper = FormHelper(self)
            self.helper.layout = Layout()
            for field_name, field in self.fields.items():
                self.helper.layout.append(Field(field_name, placeholder=field.label))
            self.helper.form_show_labels = False









