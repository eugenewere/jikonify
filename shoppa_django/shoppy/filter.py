from django.contrib.auth.models import User
import django_filters
from .models import *

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = ['category', 'brand', 'unit_cost', ]