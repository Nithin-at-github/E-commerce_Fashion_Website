from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from datetime import datetime, date, timedelta
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.shortcuts import render
from django.contrib import messages
from django.db.models import Sum
from accounts.models import *
from accounts.views import *
from cart.models import *
from shop.models import *
from .forms import *
import os

# Create your views here.

def admin_dash(request):
    if request.session.has_key('user'):
        users_count = User.objects.all().filter(is_superuser=False).count()
        start_date = datetime.now().date()
        end_date = start_date + timedelta(days=1)
        orders_today = Orders.objects.all().filter(date__range=(start_date, end_date)).count()
        tot_orders = Orders.objects.all().count()
        subcats = SubCategory.objects.all()
        categories = Category.objects.all()
        tot_sales = 0
        cash_sales = 0
        upi_sales = 0
        card_sales = 0 
        subcat_dict = {}
        monthly_revenue = {
            'January':0,
            'February':0,
            'March':0,
            'April':0,
            'May':0,
            'June':0,
            'July':0,
            'August':0,
            'September':0,
            'October':0,
            'November':0,
            'December':0,
            }
        orders = Orders.objects.all().order_by('-id')
        if orders:
            tot_sales = Orders.objects.aggregate(Sum('amount'))['amount__sum'] or 0
            cash_sales = Orders.objects.filter(payment_type='cash_on_delivery').aggregate(Sum('amount'))['amount__sum'] or 0
            upi_sales = Orders.objects.filter(payment_type='upi').aggregate(Sum('amount'))['amount__sum'] or 0
            card_sales = Orders.objects.filter(payment_type='debit-credit').aggregate(Sum('amount'))['amount__sum'] or 0

        for subcat in subcats:
            subcat_dict[subcat.name] = 0
            subcat_inst = get_object_or_404(SubCategory, pk=subcat.id)
            for order in orders:
                if order.product.sub_category == subcat_inst:
                    subcat_dict[subcat.name] += 1

        for ordr in orders:
            if ordr.date.strftime('%B') == 'January':
                monthly_revenue['January'] += ordr.amount
            elif ordr.date.strftime('%B') == 'February':
                monthly_revenue['February'] += ordr.amount
            elif ordr.date.strftime('%B') == 'March':
                monthly_revenue['March'] += ordr.amount
            elif ordr.date.strftime('%B') == 'April':
                monthly_revenue['April'] += ordr.amount
            elif ordr.date.strftime('%B') == 'May':
                monthly_revenue['May'] += ordr.amount
            elif ordr.date.strftime('%B') == 'June':
                monthly_revenue['June'] += ordr.amount
            elif ordr.date.strftime('%B') == 'July':
                monthly_revenue['July'] += ordr.amount
            elif ordr.date.strftime('%B') == 'August':
                monthly_revenue['August'] += ordr.amount
            elif ordr.date.strftime('%B') == 'September':
                monthly_revenue['September'] += ordr.amount
            elif ordr.date.strftime('%B') == 'October':
                monthly_revenue['October'] += ordr.amount
            elif ordr.date.strftime('%B') == 'November':
                monthly_revenue['November'] += ordr.amount
            elif ordr.date.strftime('%B') == 'December':
                monthly_revenue['December'] += ordr.amount
        data = {
            'user': request.user.username,
            'o_today': orders_today,
            'tot_orders': tot_orders,
            'u_count': users_count,
            'orders': orders,
            'tot_s': tot_sales,
            'cash_s': cash_sales,
            'upi_s': upi_sales,
            'card_s': card_sales,
            'subcats': subcats,
            'categories': categories,
            'subcat_dict': subcat_dict,
            'monthly_revenue': monthly_revenue,
            'domain': get_current_site(request),
        }
        return render(request, 'admin/admin_dash.html', data)
    else:
        messages.error(request, 'Please login')
        return redirect('login')

def users(request):
    if request.session.has_key('user'):
        users = User.objects.all().filter(is_superuser=False).order_by('-id')
        return render(request, 'admin/users.html',{'users':users,'domain': get_current_site(request)})
    else:
        messages.error(request, 'Please login')
        return redirect('login')

def del_user(request, uid):
    if request.session.has_key('user'):
        try:
            user = get_object_or_404(User, pk=uid)
            if user.is_superuser == False:
                Customers.objects.get(user_id=user).delete()
                User.objects.get(pk=uid).delete()
                messages.success(request,"User successfully removed.")
                return redirect('users')
            else:
                messages.error(request,"Can't delete a superuser from here !")
                return redirect('users')
        except User.DoesNotExist:
            messages.error(request,'User does not exist !')
            return redirect('users')
    else:
        messages.error(request, 'Please login')
        return redirect('login')

def categories(request):
    if request.session.has_key('user'):
        categories = Category.objects.all().order_by('-id')
        sub_cats = SubCategory.objects.all().order_by('-id')
        if request.method == 'POST':
            if 'add_subcat' in request.POST:
                name = request.POST['name']
                try:
                    SubCategory.objects.get(name=name)
                    messages.error(request,'Sub-Category already exists !')
                    return redirect('categories')
                except SubCategory.DoesNotExist:
                    subcat_form = SubCatForm(request.POST or None, request.FILES)
                    if subcat_form.is_valid():
                        subcat_form.save()
                        new_subcat = SubCategory.objects.get(name=name)
                        new_subcat.slug = slugify(name)
                        new_subcat.save()
                        messages.success(request,"New sub-category successfully added.")
                        return redirect('categories')
                    else:
                        messages.success(request,"form not valid.")
                        return redirect('categories')
            elif 'add_cat' in request.POST:
                name = request.POST.get('name')
                subcats = [x.name for x in SubCategory.objects.all()]
                subcat_ids = []
                for subcat in subcats:
                    subcat_ids.append(int(request.POST.get(subcat))) if request.POST.get(subcat) else print('')
                try:
                    SubCategory.objects.get(name=name)
                    messages.error(request,'Sub-Category already exists !')
                    return redirect('categories')
                except SubCategory.DoesNotExist:
                    cat_form = CatForm(request.POST or None, request.FILES)
                    if cat_form.is_valid():
                        cat_form.save()
                        new_cat = Category.objects.get(name=name)
                        new_cat.slug = slugify(name)
                        for subcat_id in subcat_ids:
                            new_cat.subcat.add(SubCategory.objects.get(id=subcat_id))
                        new_cat.save()
                        messages.success(request,"New category successfully added.")
                        return redirect('categories')
                    else:
                        messages.success(request,"form not valid.")
                        return redirect('categories')
        return render(request, 'admin/categories.html',{'categories':categories, 'sub_cats':sub_cats,'domain' : get_current_site(request),})
    else:
        messages.error(request, 'Please login')
        return redirect('login')

def edit_subcat(request, id):
    if request.session.has_key('user'):
        if request.method == 'POST':
            name = request.POST['name']
            desc = request.POST['desc']
            subcat = SubCategory.objects.get(id=id)
            if subcat.name != name:
                try:
                    SubCategory.objects.get(name=name)
                    messages.error(request,'Sub-Category already exists !')
                    return redirect('categories')
                except SubCategory.DoesNotExist:
                    pass
            subcat.name = name
            subcat.desc = desc
            if len(request.FILES) != 0:
                if len(subcat.img) > 0:
                    os.remove(subcat.img.path)
                subcat.img = request.FILES['img']
            subcat.slug = slugify(name)
            subcat.save()
            messages.success(request,"Sub-category successfully updated.")
            return redirect('categories')
    else:
        messages.error(request, 'Please login')
        return redirect('login')

def edit_categ(request, id):
    if request.session.has_key('user'):
        if request.method == 'POST':
            name = request.POST['name']
            cat = Category.objects.get(id=id)
            subcats = [x.name for x in SubCategory.objects.all()]
            subcat_ids = []
            for subcat in subcats:
                subcat_ids.append(int(request.POST.get(subcat))) if request.POST.get(subcat) else print('')
            if cat.name != name:
                try:
                    Category.objects.get(name=name)
                    messages.error(request,'Category already exists !')
                    return redirect('categories')
                except Category.DoesNotExist:
                    pass
            cat.name = name
            if len(request.FILES) != 0:
                if len(cat.img) > 0:
                    os.remove(cat.img.path)
                cat.img = request.FILES['img']
            cat.slug = slugify(name)
            cat.subcat.clear()
            for subcat_id in subcat_ids:
                cat.subcat.add(SubCategory.objects.get(id=subcat_id))
            cat.save()
            messages.success(request,"Category successfully updated.")
            return redirect('categories')
    else:
        messages.error(request, 'Please login')
        return redirect('login')

def brands(request):
    if request.session.has_key('user'):
        brnds = Brands.objects.all().order_by('-id')
        if request.method == 'POST':
            name = request.POST['name']
            try:
                Brands.objects.get(name=name)
                messages.error(request, 'Brand already exists !')
                return redirect('brands')
            except Brands.DoesNotExist:
                add_brand = BrandForm(request.POST or None, request.FILES)
                if add_brand.is_valid():
                    add_brand.save()
                    new_brand = Brands.objects.get(name=name)
                    new_brand.slug = slugify(name)
                    new_brand.save()
                    messages.success(request,"Successfully added brand.")
                    return redirect('brands')
        return render(request, 'admin/brands.html', {'brands':brnds,'domain' : get_current_site(request),})
    else:
        messages.error(request, 'Please login')
        return redirect('login')

def edit_brand(request, id):
    if request.session.has_key('user'):
        if request.method == 'POST':
            name = request.POST['name']
            brand = Brands.objects.get(id=id)
            if brand.name != name:
                try:
                    Brands.objects.get(name=name)
                    messages.error(request, 'Brand name already exists ! Try another one')
                    return redirect('brands')
                except Brands.DoesNotExist:
                    pass
            brand.name = name
            if len(request.FILES) != 0:
                if len(brand.logo) > 0:
                    os.remove(brand.logo.path)
                brand.logo = request.FILES['logo']
            brand.slug = slugify(name)
            brand.save()
            messages.success(request,"Successfully updated brand details.")
            return redirect('brands')
    else:
        messages.error(request, 'Please login')
        return redirect('login')

def products(request):
    if request.session.has_key('user'):
        if request.method == 'POST':
            name = request.POST.get('name')
            desc = request.POST.get('desc')
            p_form = ProductForm(request.POST or None, request.FILES)
            if p_form.is_valid():
                p_form.save()
                new_pr = Products.objects.get(name=name, desc=desc)
                new_pr.slug = slugify(name+'-'+desc)
                new_pr.save()
                messages.success(request, 'Product added successfully.')
                return redirect('products')
            else:
                messages.error(request, 'Form not valid !')
                return redirect('products')
        prdcts = Products.objects.all().order_by('-id')
        p_form = ProductForm()
        paginator = Paginator(prdcts, 12)
        try:
            page = int(request.GET.get('page','1'))
        except:
            page = 1
        try:
            pro = paginator.page(page)
        except(EmptyPage,InvalidPage):
            pro = paginator.page(paginator.num_pages)
        data = {
            'products':prdcts,
            'form':p_form,
            'domain': get_current_site(request),
            'pg': pro,
            'has_next': pro.has_next(),
            'has_previous': pro.has_previous(),
            }
        return render(request, 'admin/products.html', data)
    else:
        messages.error(request, 'Please login')
        return redirect('login')

def edit_product(request, id):
    if request.session.has_key('user'):
        product = get_object_or_404(Products, pk=id)
        if request.method == 'POST':
            name = request.POST.get('name')
            desc = request.POST.get('desc')
            p_form = ProductForm(request.POST or None, request.FILES, instance=product)
            if p_form.is_valid():
                p_form.save()
                new_pr = Products.objects.get(name=name, desc=desc)
                new_pr.slug = slugify(name+'-'+desc)
                new_pr.save()
                messages.success(request, 'Product updated successfully.')
                return redirect('products')
            else:
                messages.error(request, 'Form not valid !')
                return redirect('edit_product', id)
        pr_form = ProductForm(instance=product)
        data = {
            'id':int(id),
            'pr_form':pr_form,
            'domain': get_current_site(request),
            }
        return render(request, 'admin/edit_product.html', data)
    else:
        messages.error(request, 'Please login')
        return redirect('login')

def offers(request):
    if request.session.has_key('user'):
        offrs = Offers.objects.all().order_by('-id')
        if request.method == 'POST':
            name = request.POST.get('name')
            offer = request.POST.get('offer')
            try:
                Offers.objects.get(name=name, offer=offer)
                messages.error(request, 'Offer already exists !')
                return redirect('offers')
            except Offers.DoesNotExist:
                add_offer = OfferForm(request.POST or None, request.FILES)
                if add_offer.is_valid():
                    add_offer.save()
                    new_offer = Offers.objects.get(name=name, offer=offer)
                    new_offer.slug = slugify(name+'-'+str(offer))
                    new_offer.save()
                    messages.success(request,"Successfully added offer.")
                    return redirect('offers')
        return render(request, 'admin/offers.html', {'offers':offrs, 'domain': get_current_site(request),})
    else:
        messages.error(request, 'Please login')
        return redirect('login')

def del_offer(request, oid):
    if request.session.has_key('user'):
        try:
            Offers.objects.get(pk=oid).delete()
            messages.success(request,"Offer successfully removed.")
            return redirect('offers')
        except Offers.DoesNotExist:
            messages.error(request,'Offer does not exist !')
            return redirect('offers')
    else:
        messages.error(request, 'Please login')
        return redirect('login')

def ads(request):
    if request.session.has_key('user'):
        ad_s = Ads.objects.all().order_by('-id')
        if request.method == 'POST':
            ad_form = AdForm(request.POST or None, request.FILES)
            if ad_form.is_valid():
                ad_form.save()
                messages.success(request, 'Advertisement added')
                return redirect('ads')
        return render(request, 'admin/ads.html', {'ads':ad_s, 'domain': get_current_site(request),})
    else:
        messages.error(request, 'Please login')
        return redirect('login')

def edit_ad(request, id):
    if request.session.has_key('user'):
        if request.method == 'POST':
            name = request.POST.get('name')
            ad_date = request.POST.get('date')
            ad = Ads.objects.get(id=id)
            ad.name = name
            if len(request.FILES) != 0:
                if len(ad.img) > 0:
                    os.remove(ad.img.path)
                ad.img = request.FILES['img']
            ad.date = ad_date
            ad.save()
            messages.success(request,"Successfully updated advertisement.")
            return redirect('ads')
    else:
        messages.error(request, 'Please login')
        return redirect('login')

def reviews(request):
    if request.session.has_key('user'):
        reviws = Reviews.objects.all().order_by('-id')
        paginator = Paginator(reviws, 8)
        try:
            page = int(request.GET.get('page','1'))
        except:
            page = 1
        try:
            pro = paginator.page(page)
        except(EmptyPage,InvalidPage):
            pro = paginator.page(paginator.num_pages)
        data = {
            'reviews':reviws,
            'domain': get_current_site(request),
            'pg': pro,
            'has_next': pro.has_next(),
            'has_previous': pro.has_previous(),
            }
        return render(request, 'admin/reviews.html', data)
    else:
        messages.error(request, 'Please login')
        return redirect('login')
