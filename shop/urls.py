from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<slug:sc_slug>/', views.home, name='scprod_list'),
    path('offprod_list/<slug:o_slug>/', views.offprod_list, name='offprod_list'),
    path('products_list/<slug:c_slug>/', views.products_list, name='products_list'),
    path('product_detail/<slug:c_slug>/<slug:p_slug>/', views.product_detail, name='product_detail'),
    path('search', views.search, name='search'),
]