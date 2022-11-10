from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from shop.models import *
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def crt_id(request):
    ct_id = request.session.session_key
    if not ct_id:
        ct_id = request.session.create()
    return ct_id

def cart_details(request):
    subcats = SubCategory.objects.all()
    categories = Category.objects.all()
    tot = 0
    act_tot = 0
    tot_discount = 0
    count = 0
    try:
        ct = CartList.objects.get(cart_id=crt_id)
        ct_items = Items.objects.filter(cart=ct, active=True)
        for i in ct_items:
            prdct = Products.objects.get(id=i.product.id)
            offer = Offers.objects.get(id=prdct.offer.id)
            discount = i.product.price * (offer.offer * 0.01)
            act_price = i.product.price-int(discount)
            
            tot += (i.product.price*i.quantity)
            tot_discount += (int(discount)*i.quantity)
            act_tot += (act_price*i.quantity)
            count += i.quantity
        data = {
            'categories':categories,
            'subcats':subcats,
            'items':ct_items,
            'tot':tot,
            'act_tot': act_tot,
            'tot_discount': tot_discount,
            'count':count,
        }
    except:
        data ={
            'categories':categories,
            'subcats':subcats,
            'tot':tot,
            'act_tot': act_tot,
            'tot_discount': tot_discount,
            'count':count,
        }
    return render(request, 'cart.html', data)

def add_to_cart(request, prod_id):
    if request.method == 'POST':
        if 'quantity' in request.POST:
            quant = int(request.POST['quantity'])
        else:
            quant = 1
        p_size = request.POST['size']
        prod = Products.objects.get(id=prod_id)
        try:
            ct = CartList.objects.get(cart_id=crt_id)
        except ObjectDoesNotExist:
            ct = CartList.objects.create(cart_id=crt_id)
            ct.save()
        try:
            c_items = Items.objects.get(product=prod, cart=ct, size=p_size)
            if c_items.quantity < c_items.product.stock:
                c_items.quantity += quant
            c_items.save()
        except ObjectDoesNotExist:
            c_items = Items.objects.create(product=prod, cart=ct, size=p_size, quantity=quant)
            c_items.save()
        return redirect('cart_details')

def min_cart(request, prod_id, p_size):
    ct = CartList.objects.get(cart_id=crt_id)
    prod = get_object_or_404(Products, id=prod_id)
    c_items = Items.objects.get(product=prod, cart=ct, size=p_size)
    if c_items.quantity > 1:
        c_items.quantity -= 1
        c_items.save()
    else:
        c_items.delete()
    return redirect('cart_details')

def delete_cart(request, prod_id, p_size):
    ct = CartList.objects.get(cart_id=crt_id)
    prod = get_object_or_404(Products, id=prod_id)
    c_items = Items.objects.get(product=prod, cart=ct, size=p_size)
    
    c_items.delete()
    
    return redirect('cart_details')
