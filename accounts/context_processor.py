from .models import *
from .views import *

def wcount(request):
    w_count = 0
    if 'admin' in request.path:
        return {}
    else:
        if request.session.has_key('uid'):
            try:
                w_count = Wishlist.objects.filter(user_id=request.session['uid']).count()
            except Wishlist.DoesNotExist:
                w_count = 0
        else:
            w_count = 0
        return dict(w_count=w_count)