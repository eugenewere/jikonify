import statistics

from django import template
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render_to_response
from django.views import View
from shoppy.models import *


register = template.Library()

@register.filter(name='has_buyer_ever_ordered')
def get_buyer_orders(product_id, user):
    buyer = Buyer.objects.filter(user_ptr_id=user.id).first()
    product=Product.objects.filter(id=product_id).first()
    if buyer is not None:
        ordered_product_review=Order_Product.objects.filter(checkout__isnull=False, buyer=buyer, product=product)
        return ordered_product_review
    else:
        return False



@register.filter(name='seller_orderd_products')
def get_seller_orders( user):
    seller= Seller.objects.filter(user_ptr_id=user.id).first()
    product =Product.objects.filter(seller=seller).all()
    if seller is not None:
        check_out_orders= Order_Product.objects.filter(checkout__isnull=False, product=product)

        return check_out_orders
    else:
        return False


@register.filter(name='seller_ordered_goods')
def ordered_products(product_id, user):
    seller = Seller.objects.filter(user_ptr_id=user.id).first()
    if seller is None:
        return False
    else:
        return seller.ordered_products(product_id)

@register.filter(name='average_ratings')
def average_ratings(product_id):
    product= Product.objects.filter(id=product_id).first()
    if product is None:
        return False
    else:
        data = []
        ratings=Review.objects.filter(product=product)
        for rating in ratings:
            data.append(rating.ratings)
        if data:
            average_ratings = statistics.mean(data)

            return average_ratings
        else:
            return 0


@register.filter(name='is_seller')
def is_seller(user):
    user_id=user.id
    seller = Seller.objects.filter(user_ptr_id=user_id).first()
    if seller is None:
        return False
    else:
        return True

@register.filter(name='is_admin')
def is_admin(user):
    user_id=user.id
    user = User.objects.filter(is_superuser=True, id=user_id).first()
    if user is None:
        return False
    else:
        return True




@register.filter(name='wishlist_count')
def get_wishlist_count(user):

    buyer = Buyer.objects.filter(user_ptr_id=user.id).first()
    if buyer is not None:
        wishlist_count = Wishlist.objects.filter(buyer=buyer).count()
        return wishlist_count
    else:
        return False


@register.filter(name='is_product_in_wishlist')
def product_in_wishlist(product_id, user):
    buyer = Buyer.objects.filter(user_ptr_id=user.id).first()
    if buyer is None:
        return False
    else:
        return buyer.product_in_wishlist(product_id)


# @register.filter(name='cart_count')
# def get_cart_count(request, user):
#     session = request.COOKIES.get('Mashkys', False)
#     uzer_id=request.user.id
#     mashcookie = MashCartCookie.objects.filter(mashcookie__exact=session).first()
#     if not request.user.is_authenticated:
#         if mashcookie is not None:
#             cart_count = Order_Product.objects.filter(session_id=mashcookie.id, checkout__isnull=True, buyer_id__isnull=True).count()
#             return cart_count
#     else:
#         buyer = Buyer.objects.filter(user_ptr_id=uzer_id).first()
#         if buyer is not None:
#             cart_count =Order_Product.objects.filter(buyer=buyer, checkout__isnull=True).count()
#             return cart_count

@register.filter(name='cart_count')
def get_cart_count(request, user):
    buyer = Buyer.objects.filter(user_ptr_id=user.id).first()
    if buyer is not None:
        cart_count =Order_Product.objects.filter(buyer=buyer,checkout__isnull=True, product__wishlist__isnull=True).count()
        return cart_count
    else:
        return False

@register.filter(name='cart_count2')
def get_cart_count2(request, user):
    buyer = Buyer.objects.filter(user_ptr_id=user.id).first()
    if buyer is not None:
        cart_count =Order_Product.objects.filter(buyer=buyer,checkout__isnull=True, product__wishlist__isnull=True).count()
        return cart_count
    else:
        return False




@register.filter(name='is_product_in_cart')
def product_in_cart(product_id, user):
    buyer = Buyer.objects.filter(user_ptr_id=user.id).first()
    if buyer is None:
        return False
    else:
        return buyer.product_in_cart(product_id)


@register.filter(name='total_cost_exclusive_vat')
def total_cost_exclusive_vat(user):
    """ Total cost of cart without VAT"""
    buyer = Buyer.objects.filter(user_ptr_id=user.id).first()
    if buyer is not None:
        return buyer.cart_total
    return False


@register.filter(name='total_cost_inclusive_of_vat')
def total_cost_inclusive_of_vat(user):
    """ Total cost of cart with 16% VAT"""
    buyer = Buyer.objects.filter(user_ptr_id=user.id).first()
    if buyer is not None:
        return buyer.cart_total_plus_vat
    return False


@register.filter(name='vat_cost')
def vat_cost(user):
    """ VAT Total cost of  16% """
    buyer = Buyer.objects.filter(user_ptr_id=user.id).first()
    if buyer is not None:
        return buyer.vat_cost
    return False

@register.filter(name='categories')
def categories(request):
    categories= Category.objects.filter(parent_id__isnull=True).order_by('name')
    # children_count = Category.objects.filter(id=categories)
    if categories is not None:
        return categories
    else:
        return False

@register.filter(name='product_on_offer')
def product_on_offer(product_id):
    now = datetime.datetime.now().date()
    offers=Offer.objects.filter(product=product_id, start_time__lte=now, end_time__gte=now)
    offerz= Offer.objects.filter(product=product_id).first()
    if offers is not None:
            # if offerz.end_time < now:
            #     offerz.delete()
        return offers
    else:
        return False

@register.filter(name='if_product_is_on_offer')
def if_product_is_on_offer(product_id):
    offers=Offer.objects.filter(product=product_id)
    if offers is not None:
        return offers
    else:
        return False


@register.filter(name='make_safe')
def make_safe(source):
    source = source.replace('/', '____')
    return "%s" %source


@register.filter(name='footer_productz')
def footer_products(request):
    brandz = Brand.objects.order_by('?').first()
    productz = Product.objects.filter(product_brand=brandz).order_by("?")[:6]
    return productz
    # return {'productz':productz, 'brand':brandz}

@register.filter(name='footer_productz')
def footer_products(request):
    # brandz = Brand.objects.order_by('?').first()
    category = Category.objects.order_by('?').first()
    # productz = Product.objects.filter(product_brand_id=brandz.id).order_by("?")[:6]
    if Product.objects.filter(category_id=category.id).order_by("?").count() >= 6:
        productz = Product.objects.filter(category_id=category.id).order_by("?")[:6]
    else:
        productz = Product.objects.order_by("created_at")[:6]
    return productz
    # return {'productz':productz, 'brand':brandz}
    # return {'productz':productz, 'brand':brandz}

@register.filter(name='footer_offer_productz')
def footer_offer_products(request):
    now = datetime.datetime.now().date()
    products =[]
    offers = Offer.objects.filter( start_time__lte=now, end_time__gte=now)
    for offer in offers:
        products.append(offer.product)
    return products



@register.filter(name='footer_productz_brand')
def footer_products_brand(request):
    products = footer_products(request)[:1]
    return products
    # return {'productz':productz, 'brand':brandz}


@register.filter(name='how_to_pay_filter')
def how_to_pay_filter(request):
    user = request.user.id
    buyer = Buyer.objects.filter(user_ptr_id=user).first()
    checkout = Checkout.objects.filter(buyer=buyer, status='PENDING').order_by('-id').first()

    if checkout is not None:
        return True
    return False


@register.filter(name='variant_options')
def options(product_id, variant_id):
    vns = []
    product_variant_options = Product_Variant_Options.objects.filter(product_id=product_id)
    for option in product_variant_options:
        vns.append(option.variant_options)
    actual_variant_options = []
    for variant_option in list(set(vns)):
        if variant_option.variant_id == variant_id:
            actual_variant_options.append(variant_option)
    return list(set(actual_variant_options))

@register.filter(name='cart_variants')
def cart_variants(request, order_id ):
    variants =[]
    variant = Variant.objects.filter(variant_options__orderproductvariantoption__orderProduct_id=order_id)
    variant_options = OrderProductVariantOption.objects.filter( orderProduct__buyer=request.user.id, orderProduct_id=order_id)
    # print(variant_options)
    for option in variant_options:
        variants.append(option.variantOptions)
    # print(list(set(variants)))
    return list(set(variants))
    # print(variant_options)

@register.filter(name='order_variants')
def order_variants(order_id):
    # print(order_id)
    variants =[]
    variant_options = OrderProductVariantOption.objects.filter(orderProduct_id=order_id)
    if variant_options:
        for option in variant_options:
            variants.append(option.variantOptions)
    else:
        variants.append('No Variants Were Ordered')

    return list(set(variants))

@register.filter(name='order_total')
def order_variants(order_id):
    orderr =Order_Product.objects.filter(id=order_id).first()
    return orderr.ordertotal



@register.filter(name='seller_buyer_orders')
def seller_buyer_orders(buyer_id ):
    buyer_orders =[]
    orders=Order_Product.objects.filter(buyer_id=buyer_id, checkout__status='PENDING', checkout__isnull=False)
    for order in orders:
        buyer_orders.append(order)
    return list(set(buyer_orders))

@register.filter(name='buyer_orders_ref_code')
def buyer_orders_ref_code(buyer_id):
    orders = Order_Product.objects.filter(buyer_id=buyer_id, checkout__status='PENDING', checkout__isnull=False)
    # checkout = Checkout.objects.filter(order_product__buyer_id=buyer_id, status='PENDING',).first()
    ref_codes=[]
    for order in orders:
        ref_codes.append(order.checkout.reference_code)

    return  list(set(ref_codes))
#
@register.filter(name='buyer_orders_total')
def buyer_orders_total(reference_code ):
    # orders = Order_Product.objects.filter(buyer_id=buyer_id, checkout__status='PENDING', checkout__isnull=False).first()
    checkout = Checkout.objects.filter(order_product__buyer_id=reference_code, status__exact='PENDING').first()

    return  checkout.total

@register.filter(name='buyer_orders_date_created')
def buyer_orders_date_created(buyer_id ):
    from datetime import datetime
    # orders = Order_Product.objects.filter(buyer_id=buyer_id, checkout__status='PENDING', checkout__isnull=False).first()
    checkout = Checkout.objects.filter(order_product__buyer_id=buyer_id, status='PENDING',).first()
    if checkout:
        return  checkout.created_at
    else:
        return datetime.today()
@register.filter(name='seller_buyer_quantities')
def seller_buyer_quantities(reference_code):

    buyer_orders =[]
    orders=Order_Product.objects.filter(checkout__reference_code=reference_code).count()
    # for order in orders:
    #     buyer_orders.append(order.product)
    # # return sum(i for i in buyer_orders)
    # print(buyer_orders)
    return orders

@register.filter(name='buyers_rating_ratings')
def buyers_rating_ratings(ratings, product_id):
    buyers_count = []
    product = Product.objects.filter(id=product_id).first()
    buyer_total_ratin = Review.objects.filter(ratings=ratings, product=product)
    for review in buyer_total_ratin:
        buyers_count.append(review.buyer)
    return len(list(set(buyers_count)))


@register.filter(name='ratings_to_percentage')
def ratings_to_percentage(ratings, product_id):
    buyers_count = []
    all_buyers_count = []
    product = Product.objects.filter(id=product_id).first()
    buyer_total_ratin = Review.objects.filter(ratings=ratings, product=product)
    all_buyer_total_ratin = Review.objects.filter(product=product)

    for review in buyer_total_ratin:
        buyers_count.append(review.buyer)

    for all_review in all_buyer_total_ratin:
        all_buyers_count.append(all_review.buyer)



    lenth = len(list(set(buyers_count)))
    lenth2 = len(list(set(all_buyers_count)))
    try:
        perc = (lenth / lenth2) * 100
    except :
        perc = 0

    # print(perc)
    return perc


@register.filter(name='categoriesproducts')
def categoriesproducts(category_id):
    category = Category.objects.filter(id=category_id).first()
    products = Product.objects.filter(category=category)
    # print(category)
    # print(products)
    return products








