from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('activate/<uid64>/<token>/', views.activate, name='activate'),
    path('login', views.login, name='login'),
    path('forgot_pass', views.forgot_pass, name='forgot_pass'),
    path('reset_password/<uid64>/<token>', views.reset_password, name='reset_password'),
    path('signout', views.signout, name='signout'),
    path('wishlist', views.wishlist, name='wishlist'),
    path('add_to_wishlist/<int:prod_id>', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_wishlist/<int:prod_id>', views.remove_wishlist, name='remove_wishlist'),
    path('orders_view', views.orders_view, name='orders_view'),
    path('cancel_order/<int:order_id>', views.cancel_order, name='cancel_order'),
    path('add_review/<int:prod_id>', views.add_review, name='add_review'),
    path('edit_review/<int:review_id>', views.edit_review, name='edit_review'),
    path('del_review/<int:review_id>', views.del_review, name='del_review'),
    path('reviews_view', views.reviews_view, name='reviews_view'),
    path('profile', views.profile, name='profile'),
    path('del_account', views.del_account, name='del_account'),
]