from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User, auth
from shop.views import *
from cart.views import *

# Create your views here.

def register(request):
    if request.method == 'POST':
        uname = request.POST['uname']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        mobno = request.POST['mobno']
        address1 = request.POST['address1']
        address2 = request.POST['address2']
        city = request.POST['city']
        state = request.POST['state']
        country = request.POST['country']
        zipcode = request.POST['zipcode']

        if password == cpassword:
            if User.objects.filter(username=uname).exists():
                messages.error(request, "Username already exists..! Try another one.")
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email id already exists..! Try another one.")
                return redirect('register')
            else:
                create_user = User.objects.create_user(
                    username=uname,
                    password=cpassword,
                    email=email,
                    first_name=fname,
                    last_name=lname
                )
                create_user.save()
                try:
                    user = get_object_or_404(User, username=uname)
                    customer = Customers.objects.create(
                        user_id= user,
                        firstname=fname,
                        lastname=lname,
                        email=email,
                        mob_no=mobno,
                        address_line1=address1,
                        address_line2=address2,
                        city=city,
                        state=state,
                        country=country,
                        zip_code=zipcode
                    )
                    customer.save()
                    messages.success(request, "Registration Successfull. Try Login.")
                    return redirect('login')
                except User.DoesNotExist:
                    messages.error(request, "Something went wrong..! Try again.")
                    return redirect('register')
        else:
            messages.error(request, "Passwords not matching.")
            return redirect('register')
    return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        uname = request.POST['uname']
        password = request.POST['password']

        user = authenticate(username=uname, password=password)
        if user is not None:
            auth.login(request, user)
            request.session['uid'] = user.id
            return redirect('home')
        else:
            messages.error(request, 'Incorrect username or password.')
            return redirect('login')
    return render(request, 'signin.html')

def signout(request):
    logout(request)
    if request.session.has_key('uid'):
        del request.session['uid']
    messages.success(request, 'Logged out successfully.')
    return redirect('home')

def wishlist(request):
    if request.session.has_key('uid'):
        wlist = Wishlist.objects.all().filter(user_id=request.session['uid'])
        return render(request, 'wishlist.html', {'w_list': wlist})
    else:
        messages.error(request, 'Please sign in to get access to wishlist.')
        return redirect('login')

def add_to_wishlist(request, prod_id):
    if request.session.has_key('uid'):
        user = get_object_or_404(User, id=request.session['uid'])
        product = get_object_or_404(Products, id=prod_id)
        try:
            prdct = Wishlist.objects.get(user_id=user, product=product)
            if prdct:
                messages.warning(request, "This product is already in your wishlist.")
                return redirect('wishlist')
        except Wishlist.DoesNotExist:
            wlist = Wishlist.objects.create(user_id=user, product=product)
            wlist.save()
            messages.success(request, 'Product saved to wishlist successfully')
            return redirect('wishlist')
    else:
        messages.error(request, 'Please sign in to get access to wishlist.')
        return redirect('login')

def remove_wishlist(request, prod_id):
    if request.session.has_key('uid'):
        try:
            user = get_object_or_404(User, id=request.session['uid'])
            product = get_object_or_404(Products, id=prod_id)
            prdct = Wishlist.objects.get(user_id=user, product=product)
            prdct.delete()
            messages.success(request, "Product successfully removed from wishlist.")
            return redirect('wishlist')
        except Wishlist.DoesNotExist:
            messages.error(request, "Something unexpected happened ! Try again later.")
            return redirect('wishlist')

def orders_view(request):
    if request.session.has_key('uid'):
        orders = Orders.objects.all().filter(cart=request.session['uid'])
        return render(request, 'orders.html',{'orders':orders})
    else:
        messages.error(request, 'Please sign in to see your orders.')
        return redirect('login')

def profile(request):
    pass
