from django.urls import path
from . import views

urlpatterns = [
    path('cart_details', views.cart_details, name='cart_details'),
    path('add_to_cart/<int:prod_id>', views.add_to_cart, name='add_to_cart'),
    path('min_cart/<int:prod_id>/<p_size>', views.min_cart, name='min_cart'),
    path('delete_cart/<int:prod_id>/<p_size>', views.delete_cart, name='delete_cart'),
]