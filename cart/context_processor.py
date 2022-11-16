from .models import *
from .views import *

def count(request):
    itm_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            if request.session.has_key('uid'):
                ct = CartList.objects.filter(cart_id=request.session['uid'])
            else:
                ct = CartList.objects.filter(cart_id=crt_id(request))
            cti = Items.objects.all().filter(cart=ct[:1])
            for c in cti:
                itm_count += c.quantity
        except CartList.DoesNotExist:
            itm_count = 0
        return dict(item_count=itm_count)