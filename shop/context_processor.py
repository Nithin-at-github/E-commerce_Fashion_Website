from .models import *
from .views import *
from django.contrib.auth.models import User

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
