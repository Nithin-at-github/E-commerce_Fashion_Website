from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from shop.models import *
from accounts.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from datetime import datetime
import random, string
# Create your views here.

def crt_id(request):
    if not request.session.has_key('guest'):
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(8))
        request.session['guest'] = result_str
        ct_id = request.session['guest']
    else:
        ct_id = request.session['guest']
    return ct_id

def cart_details(request):
    tot = 0
    act_tot = 0
    tot_discount = 0
    tot_shipping = 0
    count = 0
    try:
        if request.session.has_key('uid'):
            ct_id = request.session['uid']
            ct = CartList.objects.get(cart_id=ct_id)
        else:
            ct_id = crt_id(request)
            ct = CartList.objects.get(cart_id=crt_id(request))
        ct_items = Items.objects.filter(cart=ct, active=True)
        if ct_items.count() == 0:
            data = {
                'items': ct_items,
                'tot': tot,
                'act_tot': act_tot,
                'tot_discount': tot_discount,
                'tot_shipping': tot_shipping,
                'count': count,
            }
        else:
            for i in ct_items:
                prdct = Products.objects.get(id=i.product.id)
                offer = Offers.objects.get(id=prdct.offer.id)
                discount = i.product.price * (offer.offer * 0.01)
                act_price = int(i.product.price-discount)
                
                tot += (i.product.price*i.quantity)
                tot_discount += int(discount*i.quantity)
                tot_shipping += (prdct.shipping*i.quantity)
                if (act_tot+act_price*i.quantity) > 500:
                    act_tot += int(act_price*i.quantity)
                else:    
                    act_tot += int(act_price*i.quantity) + tot_shipping
                count += i.quantity
            data = {
                'ct_id': ct_id,
                'items': ct_items,
                'tot': tot,
                'act_tot': act_tot,
                'tot_discount': tot_discount,
                'tot_shipping': tot_shipping,
                'count': count,
            }
    except CartList.DoesNotExist:
        data ={
            'tot': tot,
            'act_tot': act_tot,
            'tot_discount': tot_discount,
            'tot_shipping': tot_shipping,
            'count': count,
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
        if request.session.has_key('uid'):
            try:
                ct = CartList.objects.get(cart_id=request.session['uid'])
            except ObjectDoesNotExist:
                ct = CartList.objects.create(cart_id=request.session['uid'])
                ct.save()
        else:
            try:
                ct = CartList.objects.get(cart_id=crt_id(request))
            except ObjectDoesNotExist:
                ct = CartList.objects.create(cart_id=crt_id(request))
                ct.save()
        try:
            c_items = Items.objects.get(product=prod, cart=ct, size=p_size)
            if c_items.quantity < c_items.product.stock:
                c_items.quantity += quant
            c_items.save()
            return redirect('cart_details')
        except ObjectDoesNotExist:
            c_items = Items.objects.create(product=prod, cart=ct, size=p_size, quantity=quant)
            c_items.save()
            messages.success(request, "Product added to cart successfully. Check out the cart to proceed buying.")
            return redirect('product_detail', prod.category.slug, prod.slug)

def min_cart(request, prod_id, p_size):
    if request.session.has_key('uid'):
        ct = CartList.objects.get(cart_id=request.session['uid'])
    else:
        ct = CartList.objects.get(cart_id=crt_id(request))
    prod = get_object_or_404(Products, id=prod_id)
    c_items = Items.objects.get(product=prod, cart=ct, size=p_size)
    if c_items.quantity > 1:
        c_items.quantity -= 1
        c_items.save()
    else:
        c_items.delete()
        if request.session.has_key('guest'):
            c = Items.objects.all().filter(cart=ct).count()
            if c == 0:
                ct.delete()
                del request.session['guest']
    return redirect('cart_details')

def delete_cart(request, prod_id, p_size):
    if request.session.has_key('uid'):
        ct = CartList.objects.get(cart_id=request.session['uid'])
    else:
        ct = CartList.objects.get(cart_id=crt_id(request))
    prod = get_object_or_404(Products, id=prod_id)
    c_items = Items.objects.get(product=prod, cart=ct, size=p_size)
    c_items.delete()
    
    if not request.session.has_key('uid'):
        c = Items.objects.all().filter(cart=ct).count()
        if c == 0:
            ct.delete()
    return redirect('cart_details')

def checkout(request):
    tot = 0
    act_tot = 0
    tot_shipping = 0
    customer = None
    try:
        if request.session.has_key('uid'):
            c_id = request.session['uid']
            cart = CartList.objects.get(cart_id=c_id)
            customer = Customers.objects.get(user_id=c_id)
        elif request.session.has_key('guest'):
            c_id = crt_id(request)
            cart = CartList.objects.get(cart_id=crt_id(request))
        else:
            return redirect('cart_details')
        cart_obj = get_object_or_404(CartList,id=cart.id)
        products = Items.objects.all().filter(cart=cart_obj)
        for i in products:
            prdct = Products.objects.get(id=i.product.id)
            offer = Offers.objects.get(id=prdct.offer.id)
            discount = i.product.price * (offer.offer * 0.01)
            act_price = int(i.product.price-discount)

            tot += (act_price*i.quantity)
            tot_shipping += (prdct.shipping*i.quantity)
            if (act_tot+tot) > 500:
                act_tot += (act_price*i.quantity)
            else:    
                act_tot += (act_price*i.quantity) + tot_shipping
            data = {
                'cid':c_id,
                'customer':customer,
                'items':products,
                'tot':tot,
                'tot_shipping':tot_shipping,
                'act_tot':act_tot,
            }
        if request.method == 'POST':
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            email = request.POST['email']
            mob_no = request.POST['mob_no']
            address_line1 = request.POST['address_line1']
            address_line2 = request.POST['address_line2']
            city = request.POST['city']
            state = request.POST['state']
            country = request.POST['country']
            zip_code = request.POST['zip_code']
            payment_type = request.POST['payment_type']
            
            for i in products:
                for j in range(i.quantity):
                    pro = Products.objects.get(id=i.product.id)
                    offr = Offers.objects.get(id=pro.offer.id)
                    discnt = i.product.price * (offr.offer * 0.01)
                    act_price = (i.product.price-round(discnt))
                    if (act_price*i.quantity) < 500:
                        tot_amount = act_price + i.product.shipping
                    else:
                        tot_amount = act_price
                    pr_obj = get_object_or_404(Products,id=i.product.id)
                    order = Orders.objects.create(
                        cart= c_id,
                        product=pr_obj,
                        size=i.size,
                        amount=tot_amount,
                        firstname=firstname,
                        lastname=lastname,
                        email=email,
                        mob_no=mob_no,
                        address_line1=address_line1,
                        address_line2=address_line2,
                        city=city,
                        state=state,
                        country=country,
                        zip_code=zip_code,
                        payment_type=payment_type,
                        date = datetime.now(),
                        status='Order Placed',
                    )
                    order.save()
            if request.session.has_key('uid'):
                ct = CartList.objects.get(cart_id=request.session['uid'])
                Items.objects.filter(cart=ct).delete()
            elif request.session.has_key('guest'):
                ct = CartList.objects.get(cart_id=crt_id(request))
                ct.delete()
                del request.session['guest']
            return render(request, 'order_success.html')
        else:
            return render(request, 'checkout.html', data)
    except CartList.DoesNotExist:
        return redirect('cart_details')
