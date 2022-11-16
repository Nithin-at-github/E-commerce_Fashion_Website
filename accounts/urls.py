from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('signout', views.signout, name='signout'),
    path('wishlist', views.wishlist, name='wishlist'),
    path('add_to_wishlist/<int:prod_id>', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_wishlist/<int:prod_id>', views.remove_wishlist, name='remove_wishlist'),
    path('orders_view', views.orders_view, name='orders_view'),
    path('profile', views.profile, name='profile'),
]