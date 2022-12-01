from ecomm_project import settings
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .tokens import generate_token
from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User, auth
from shop.views import *
from cart.views import *
from django.core.mail import send_mail, EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from datetime import datetime

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
    page = 'login'
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
    return render(request, 'signin.html', {'page': page})

def forgot_pass(request):
    page = 'forgot_pass'
    if request.method == 'POST':
        username = request.POST['uname']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None
            
        if user != None:
            # Reset mail
            current_site = get_current_site(request)
            email_sub = "Reset Password"
            message = render_to_string("reset_pass_mail.html",{
                'user' : user.first_name,
                'domain' : current_site.domain,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : generate_token.make_token(user),
            })
            email = EmailMessage(
                email_sub,
                message,
                settings.EMAIL_HOST_USER,
                [user.email],
            )
            email.fail_silently=False
            email.send()
            messages.success(request, "Password reset link has been sent. Please check your mail")
            return redirect('forgot_pass')
        else:
            messages.error(request, "Username doesn't match any accounts.")
            return redirect('forgot_pass')
    else:
        return render(request, 'signin.html', {'page': page})

def reset_password(request, uid64, token):
    if request.method == 'POST':
        uid =force_str(urlsafe_base64_decode(uid64))
        passwd = request.POST['password']
        cpasswd = request.POST['cpassword']

        if passwd != cpasswd:
            messages.error(request, "Passwords not matching !")
            return redirect('reset_password', uid64, token)
        else:
            user = User.objects.get(pk=uid)
            user.set_password(cpasswd)
            user.save()
            messages.success(request, "Password reseted successfully. Try login.")
            return redirect('login')
    else:
        try:
            uid =force_str(urlsafe_base64_decode(uid64))
            myuser = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            myuser = None
        
        if myuser is not None and generate_token.check_token(myuser, token):
            page = 'reset_pass'
            return render(request, 'signin.html', {'uid':uid64, 'token':token, 'page':page})

def signout(request):
    logout(request)
    if request.session.has_key('uid'):
        del request.session['uid']
    messages.success(request, 'Logged out successfully.')
    return redirect('home')

def wishlist(request):
    if request.session.has_key('uid'):
        wlist = Wishlist.objects.all().filter(user_id=request.session['uid']).order_by('-id')
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
        orders = Orders.objects.all().filter(cart=request.session['uid']).order_by('-id')
        return render(request, 'orders.html',{'orders':orders})
    else:
        messages.error(request, 'Please sign in to see your orders.')
        return redirect('login')

def cancel_order(request, order_id):
    order = Orders.objects.get(pk=order_id)
    
    if order.size == 'XS':
        updated_stock = order.product.stock_xs + 1
        Products.objects.filter(pk=order.product.id).update(stock_xs=updated_stock)
    elif order.size == 'S':
        updated_stock = order.product.stock_s + 1
        Products.objects.filter(pk=order.product.id).update(stock_s=updated_stock)
    elif order.size == 'M':
        updated_stock = order.product.stock_m + 1
        Products.objects.filter(pk=order.product.id).update(stock_m=updated_stock)
    elif order.size == 'L':
        updated_stock = order.product.stock_l + 1
        Products.objects.filter(pk=order.product.id).update(stock_l=updated_stock)
    elif order.size == 'XL':
        updated_stock = order.product.stock_xl + 1
        Products.objects.filter(pk=order.product.id).update(stock_xl=updated_stock)
    
    Orders.objects.filter(pk=order_id).delete()
    messages.success(request, "Order cancelled..!")
    return redirect('orders_view')

def add_review(request, prod_id):
    product = Products.objects.get(pk=prod_id)
    c_slug = product.category.slug
    p_slug = product.slug
    prod = get_object_or_404(Products, pk=prod_id)
    if request.session.has_key('uid'):
        user = get_object_or_404(User, pk=request.session['uid'])
        orders = Orders.objects.filter(cart=request.session['uid'],product=prod)
        if orders:
            try:
                is_in_review = Reviews.objects.get(user=user,product=prod)
                if is_in_review:
                    messages.error(request, "You've already added a review for this product.")
                    return redirect('product_detail', c_slug, p_slug)
            except Reviews.DoesNotExist:    
                if request.method == 'POST':
                    name = request.POST['name']
                    email = request.POST['email']
                    rating = request.POST['rating']
                    comment = request.POST['comment']

                    if rating == '':
                        messages.error(request, 'Please provide star rating for this product.')
                        return redirect('product_detail', c_slug, p_slug)

                    review = Reviews.objects.create(
                                user=user,
                                product=prod,
                                name=name,
                                email=email,
                                comment=comment,
                                rating=rating
                            )
                    review.save()
                    cur_avg = product.avg_review
                    cur_no_reviews = product.tot_reviews
                    updated_avg = (cur_avg + int(rating)) / (cur_no_reviews + 1)
                    product.avg_review = updated_avg
                    product.tot_reviews += 1
                    product.save(update_fields=['avg_review','tot_reviews'])
                    messages.success(request, 'Your review has been successfully added. Thank you for your review.')
                    return redirect('product_detail', c_slug, p_slug)
        else:
            messages.error(request, 'You must purchase this product to add a review.')
            return redirect('product_detail', c_slug, p_slug)
    else:
        messages.error(request, 'Only registered users can add reviews. Please sign in/sign up')
        return redirect('product_detail', c_slug, p_slug)

def reviews_view(request):
    if request.session.has_key('uid'):
        reviews = Reviews.objects.all().filter(user=request.session['uid']).order_by('-last_updated')
        data = {'reviews': reviews}
        return render(request, 'view_reviews.html', data)
    else:
        messages.error(request, 'Please sign in see reviews.')
        return redirect('login')

def edit_review(request, review_id):
    review = Reviews.objects.get(pk=review_id)
    reviews = Reviews.objects.all().filter(user=request.session['uid']).order_by('-last_updated')
    if request.method == 'POST':
        rating = request.POST['rating']
        comment = request.POST['comment']

        product = Products.objects.get(pk=review.product.id)
        cur_avg = product.avg_review * product.tot_reviews
        if not product.tot_reviews == 1:
            new_avg = (cur_avg - review.rating) / (product.tot_reviews - 1)
        else:
            new_avg = 0

        updated_avg = (new_avg + int(rating)) / product.tot_reviews
        product.avg_review = updated_avg
        product.save(update_fields=['avg_review'])

        review.rating = rating
        review.comment = comment
        review.edited = True
        review.last_updated = datetime.now()

        review.save(update_fields=['rating', 'comment', 'edited', 'last_updated'])
        messages.success(request, 'Review successfully updated.')
        return redirect('reviews_view')
    return render(request, 'view_reviews.html', {'e_review': review, 'reviews': reviews})

def del_review(request, review_id):
    if request.session.has_key('uid'):
        review = Reviews.objects.get(pk=review_id)
        if review.user.id == request.session['uid']:
            product = Products.objects.get(pk=review.product.id)
            cur_avg = product.avg_review
            cur_no_reviews = product.tot_reviews
            if cur_no_reviews == 1:
                updated_avg = cur_avg - review.rating
            else:
                updated_avg = (cur_avg - review.rating) / (cur_no_reviews - 1)
            product.avg_review = updated_avg
            product.tot_reviews -= 1
            product.save(update_fields=['avg_review','tot_reviews'])
            review.delete()
            messages.success(request, 'Review successfully removed.')
            return redirect('reviews_view')
        else:
            messages.error(request, 'You can only delete your reviews.')
            return redirect('reviews_view')

def profile(request):
    if request.session.has_key('uid'):
        user = get_object_or_404(User, pk=request.session['uid'])
        customer = Customers.objects.get(user_id=user)
        mode = 'view'
        if request.method == 'POST':
            if "edit" in request.POST:
                mode = 'edit'
                data = {
                    'customer': customer,
                    'mode': mode
                }
            else:
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

                User.objects.filter(pk=request.session['uid']).update(
                    email = email,
                    first_name = fname,
                    last_name = lname
                )
                Customers.objects.filter(pk=customer.id).update(
                    firstname = fname,
                    lastname = lname,
                    email = email,
                    mob_no = mobno,
                    address_line1 = address2,
                    address_line2 = address1,
                    city = city,
                    state = state,
                    country = country,
                    zip_code = zipcode,
                )
                messages.success(request, 'Details updated successfully.')
                return redirect('profile')
        else:
            data = {
                'customer': customer,
            }
        return render(request, 'profile.html', data)
    else:
        messages.error(request, 'Please sign in to access profile.')
        return redirect('login')
