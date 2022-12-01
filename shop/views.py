from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.db.models import Q
from functools import reduce
from accounts.models import *
from cart.models import *
from .models import *
import operator

# Create your views here.

def home(request, sc_slug=None):
    subcat = None
    products = None
    
    if sc_slug != None:
        subcat = get_object_or_404(SubCategory, slug=sc_slug)
        products = Products.objects.filter(sub_category=subcat, available=True).order_by('-id')
        paginator = Paginator(products,12)
        try:
            page = int(request.GET.get('page','1'))
        except:
            page = 1
        try:
            pro = paginator.page(page)
        except(EmptyPage,InvalidPage):
            pro = paginator.page(paginator.num_pages)
        data = {
            'products':products,
            'pg': pro,
            'has_next': pro.has_next(),
            'has_previous': pro.has_previous(),
        }
        return render(request, 'products.html', data)
    else:
        products = Products.objects.all().filter(available=True).order_by('-id')
        sc_count = SubCategory.objects.all().count()
        f_products = Products.objects.all().filter(available=True,featured=True)
        brands = Brands.objects.all().order_by('-id')
        offers = Offers.objects.all().order_by('-id')
        ads = Ads.objects.all().order_by('-id')
        ad_count = Ads.objects.all().count()
        data = {
            'sc_count': range(sc_count),
            'products':products,
            'f_products':f_products,
            'brands':brands,
            'offers':offers,
            'ads':ads,
            'ad_count': range(ad_count),
        }
        return render(request, 'index.html', data)

def products_list(request, c_slug):
    c_page = get_object_or_404(Category, slug=c_slug)
    products = Products.objects.filter(category=c_page, available=True).order_by('-id')
    paginator = Paginator(products,12)
    try:
        page = int(request.GET.get('page','1'))
    except:
        page = 1
    try:
        pro = paginator.page(page)
    except(EmptyPage,InvalidPage):
        pro = paginator.page(paginator.num_pages)
    data = {
        'products':products,
        'pg': pro,
        'has_next': pro.has_next(),
        'has_previous': pro.has_previous(),
    }
    return render(request, 'products.html', data)

def offprod_list(request, o_slug):
    offer = get_object_or_404(Offers, slug=o_slug)
    products = Products.objects.filter(offer=offer, available=True).order_by('-id')
    paginator = Paginator(products,12)
    try:
        page = int(request.GET.get('page','1'))
    except:
        page = 1
    try:
        pro = paginator.page(page)
    except(EmptyPage,InvalidPage):
        pro = paginator.page(paginator.num_pages)
    data = {
        'products':products,
        'pg': pro,
        'has_next': pro.has_next(),
        'has_previous': pro.has_previous(),
    }
    return render(request, 'products.html', data)

def product_detail(request, c_slug, p_slug):
    try:
        product = Products.objects.get(category__slug=c_slug, slug=p_slug)
        c_page = get_object_or_404(Category, slug=c_slug)
        product_inst = get_object_or_404(Products, pk=product.id)
        suggestions = Products.objects.filter(category=c_page, available=True)
        reviews =  Reviews.objects.all().filter(product=product_inst).order_by('-id')
        reviews_count = reviews.count()
    except Exception as e:
        return e
    data = {
        'c_slug': c_slug,
        'product': product,
        'suggestions': suggestions,
        'reviews': reviews,
        'r_count': reviews_count,
    }
    return render(request, 'detail.html', data)

def search(request):        
    products = None
    query = None
    color = []
    price = []
    lbounds =[]
    ubounds =[]
    querys = []
    if 'qry' in request.GET:
        query = request.GET.get('qry')
        if request.method == 'POST':
            price = request.POST.getlist('price')
            color = request.POST.getlist('color')

            if not price:
                price = ['all']
            if not color:
                color = ['all']

            if 'all' in color and 'all' in price:
                products = Products.objects.all().filter(Q(name__contains=query)|Q(desc__contains=query)).order_by('-id')
            elif 'all' in color and 'all' not in price:
                if 'above' in price:
                    price.remove('above')
                    for p in price:
                        limit = p.split('-')
                        lbound = int(limit[0])
                        lbounds.append(lbound)
                        ubound = int(limit[1])
                        ubounds.append(ubound)
                    count = len(price)
                    price.append('above')
                    querys = [Q(price__range=[lbounds[i],ubounds[i]]) for i in range(0,count)]
                    if querys:
                        arg = reduce(operator.or_, querys)
                    else:
                        arg = Q()
                    products = Products.objects.all().filter(
                                Q(name__contains=query)|Q(desc__contains=query),
                                arg|Q(price__gte=3000)
                                ).order_by('-id')
                else:
                    for p in price:
                        limit = p.split('-')
                        lbound = int(limit[0])
                        lbounds.append(lbound)
                        ubound = int(limit[1])
                        ubounds.append(ubound)
                    count = len(price)
                    querys = [Q(price__range=[lbounds[i],ubounds[i]]) for i in range(0,count)]
                    arg = reduce(operator.or_, querys)
                    products = Products.objects.all().filter(
                                Q(name__contains=query)|Q(desc__contains=query),
                                arg
                                ).order_by('-id')
            elif 'all' in price and 'all' not in color:
                products = Products.objects.all().filter(
                            Q(name__contains=query)|Q(desc__contains=query),
                            Q(color__in=color)|Q(sec_color__in=color)
                            ).order_by('-id')
            elif 'all' not in price and 'all' not in color and 'above' in price:
                price.remove('above')
                for p in price:
                    limit = p.split('-')
                    lbound = int(limit[0])
                    lbounds.append(lbound)
                    ubound = int(limit[1])
                    ubounds.append(ubound)
                count = len(price)
                price.append('above')
                querys = [Q(price__range=[lbounds[i],ubounds[i]]) for i in range(0,count)]
                if querys:
                    arg = reduce(operator.or_, querys)
                else:
                    arg = Q()
                products = Products.objects.all().filter(
                            Q(name__contains=query)|Q(desc__contains=query),
                            arg|Q(price__gte=3000),
                            Q(color__in=color)|Q(sec_color__in=color)
                            ).order_by('-id')
            else:
                for p in price:
                    limit = p.split('-')
                    lbound = int(limit[0])
                    lbounds.append(lbound)
                    ubound = int(limit[1])
                    ubounds.append(ubound)
                count = len(price)
                querys = [Q(price__range=[lbounds[i],ubounds[i]]) for i in range(0,count)]
                arg = reduce(operator.or_, querys)
                products = Products.objects.all().filter(
                            Q(name__contains=query)|Q(desc__contains=query),
                            arg,
                            Q(color__in=color)|Q(sec_color__in=color)
                            ).order_by('-id')
        else:
            products = Products.objects.all().filter(Q(name__contains=query)|Q(desc__contains=query)).order_by('-id')
        if products.exists():
            paginator = Paginator(products,15)
            try:
                page = int(request.GET.get('page','1'))
            except:
                page = 1
            try:
                pro = paginator.page(page)
            except(EmptyPage,InvalidPage):
                pro = paginator.page(paginator.num_pages)
            data = {
                'qry': query,
                'products': products,
                'pg': pro,
                'has_next': pro.has_next(),
                'has_previous': pro.has_previous(),
                'color':color,
                'price':price,
            }
            return render(request, 'search.html', data)
        else:
            return render(request, 'search_error.html', {'qry':query,})
