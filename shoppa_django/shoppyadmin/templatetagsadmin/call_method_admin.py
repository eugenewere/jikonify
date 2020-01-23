
from django import template
from shoppy.models import *

register = template.Library()

# @register.filter(name='is_seller_verified')
# def get_buyer_orders(seller_id):
#     seller= Seller.objects.filter(id=seller_id).first()

