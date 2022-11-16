from django import template
from shop.models import *

register = template.Library()

def catfilter(cat, subcateg):
    return cat.filter(subcat=subcateg)

def remove_obj(list, slug):
    return list.exclude(slug=slug).order_by('-id')[:4]

def times(num):
    return range(num)

register.filter('catfilter', catfilter)
register.filter('remove_obj', remove_obj)
register.filter('times', times)