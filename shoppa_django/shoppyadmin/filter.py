from django.contrib.auth.models import User
import django_filters
from shoppy.models import *

class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', ]

class SellerProductFilter(django_filters.FilterSet):
    # year_joined = django_filters.NumberFilter(name='date_joined', lookup_expr='year')
    class Meta:
        model = Product
        fields = ['seller',]