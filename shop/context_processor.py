from .models import *
from .views import *

def navbar(request):
    if 'admin' in request.path:
        return {}
    else:
        subcats = SubCategory.objects.all()
        categories = Category.objects.all()
        data = {
                'categories':categories,
                'subcats':subcats,
            }
        return data
