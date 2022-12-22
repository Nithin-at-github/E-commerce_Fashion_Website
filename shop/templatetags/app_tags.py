from django import template
from shop.models import *

register = template.Library()

def catfilter(cat, subcateg):
    return cat.filter(subcat=subcateg)

def remove_obj(list, slug):
    return list.exclude(slug=slug).order_by('-id')[:4]

def times(num):
    return range(round(num))

def rating_rem(num):
    new_range = 5-round(num)
    return range(new_range)

def get_dict(dictnry, key):
    return dictnry.get(key)

register.filter('catfilter', catfilter)
register.filter('remove_obj', remove_obj)
register.filter('times', times)
register.filter('rating_rem', rating_rem)
register.filter('get_dict', get_dict)