from django.shortcuts import get_object_or_404, render
from .models import *
from cart.models import *
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, InvalidPage

# Create your views here.

def home(request, sc_slug=None):
    subcat = None
    products = None
    if sc_slug != None:
        subcat = get_object_or_404(SubCategory, slug=sc_slug)
        products = Products.objects.filter(sub_category=subcat, available=True)
        paginator = Paginator(products,6)
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
            'pg': pro
        }
        return render(request, 'shop.html', data)
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
    products = Products.objects.filter(category=c_page, available=True)
    paginator = Paginator(products,6)
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
        'pg': pro
    }
    return render(request, 'shop.html', data)

def offprod_list(request, o_slug):
    offer = get_object_or_404(Offers, slug=o_slug)
    products = Products.objects.filter(offer=offer, available=True)
    paginator = Paginator(products,6)
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
        'pg': pro
    }
    return render(request, 'shop.html', data)

def product_detail(request, c_slug, p_slug):
    try:
        product = Products.objects.get(category__slug=c_slug, slug=p_slug)
        c_page = get_object_or_404(Category, slug=c_slug)
        suggestions = Products.objects.filter(category=c_page, available=True)
    except Exception as e:
        return e
    data = {
        'c_slug': c_slug,
        'product': product,
        'suggestions': suggestions,
    }
    return render(request, 'detail.html', data)

def search(request):
    products = None
    query = None
    if 'qry' in request.GET:
        query = request.GET.get('qry')
        products = Products.objects.all().filter(Q(name__contains=query)|Q(desc__contains=query))
        if products.exists():
            paginator = Paginator(products,6)
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
            }
            return render(request, 'shop.html', data)
        else:
            return render(request, 'search_error.html', {'qry':query,})











