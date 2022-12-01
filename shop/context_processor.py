from .models import *
from .views import *
from django.contrib.auth.models import User
from django.db.models import Max

def navbar(request):
    if 'admin' in request.path:
        return {}
    else:
        subcats = SubCategory.objects.all()
        categories = Category.objects.all()
        user = None
        if request.session.has_key('uid'):
            user = User.objects.get(id=request.session['uid'])
        data = {
                'categories': categories,
                'subcats': subcats,
                'user': user,
            }
        return data

def filter(request):
    if 'admin' in request.path:
        return {}
    else:
        prices = []
        products = Products.objects.all()
        for i in products:
            prdct = Products.objects.get(id=i.id)
            offer = Offers.objects.get(id=prdct.offer.id)
            discount = i.price * (offer.offer * 0.01)
            act_price = int(i.price-discount)
            prices.append(act_price)
        colors = Products.objects.filter().values('color').distinct()
        sec_colors = Products.objects.filter().values('sec_color').distinct()
        tot_colors = colors.union(sec_colors)
        return {'max_price':max(prices), 'colors':tot_colors,}









