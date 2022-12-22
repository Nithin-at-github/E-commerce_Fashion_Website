from django.urls import path
from . import views

urlpatterns = [
    path('admin_dash', views.admin_dash, name='admin_dash'),
    path('users', views.users, name='users'),
    path('del_user/<int:uid>', views.del_user, name='del_user'),
    path('categories', views.categories, name='categories'),
    path('edit_subcat/<int:id>', views.edit_subcat, name='edit_subcat'),
    path('edit_categ/<int:id>', views.edit_categ, name='edit_categ'),
    path('brands', views.brands, name='brands'),
    path('edit_brand/<int:id>', views.edit_brand, name='edit_brand'),
    path('products', views.products, name='products'),
    path('edit_product/<int:id>', views.edit_product, name='edit_product'),
    path('offers', views.offers, name='offers'),
    path('del_offer/<int:oid>', views.del_offer, name='del_offer'),
    path('ads', views.ads, name='ads'),
    path('edit_ad/<int:id>', views.edit_ad, name='edit_ad'),
    path('reviews', views.reviews, name='reviews'),
]