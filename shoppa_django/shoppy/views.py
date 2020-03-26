import json
import os

import sweetify

from androidAuthApi.models import ShortCode
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth import authenticate, logout, login, get_user_model
from django.utils.crypto import get_random_string
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
import africastalking
from django_project import settings
from django.views.decorators.csrf import csrf_exempt
from requests import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from .forms import *


# Create your views here.

# # Base method with no type specified
# sweetify.sweetalert(self.request, 'Westworld is awesome', text='Really... if you have the chance - watch it!' persistent='I agree!')
#
# # Additional methods with the type already defined
# sweetify.info(self.request, 'Message sent', button='Ok', timer=3000)
# sweetify.success(self.request, 'You successfully changed your password')
# sweetify.error(self.request, 'Some error happened here - reload the site', persistent=':(')
# sweetify.warning(self.request, 'This is a warning... I guess')




def search(request):

    if request.method=="POST":
        search_text = request.POST['search_text']
        print(search_text)
    else:
        search_text =""

    products = Product.objects.filter(name__contains=search_text, status='VERIFIED' )
    context={
        'products': products,
        'search_text': search_text,
    }
    return render_to_response('shoppy/search.html',context)

def home(request):
    user = request.user
    carousels =Carousel.objects.order_by("-created_at")
    brand = Brand.objects.order_by('?').first()
    products = Product.objects.order_by("?")
    featured_products = Product.objects.filter(feat_product='FEATURED', status='VERIFIED')
    products_all = Product.objects.filter(status='VERIFIED').order_by('?')
    wishlist_count = Wishlist.objects.filter(buyer_id=request.user.id).count()
    brand_products = Product.objects.filter(product_brand=brand).order_by("?")
    # mod = os.path.dirname(__file__)
    # file = os.path.join(mod, 'county.json')
    #
    # with open(file) as f:
    #     print()
    #     data = f.read()
    #     # print(data.split('¿', 1)[1])
    #     json_data = json.loads(data.split('¿', 1)[1])
    #
    #     for p in json_data:
    #         County.objects.create(
    #            number=p['county_number'],
    #            name=p['county']
    #
    #         )
            # print(p['county_number'], p['county'])


    context ={
        'title':'Mashkys',
        'user': user,
        'carousels' : carousels,
        'featured_products': featured_products,
        # 'products': products,
        'product_brands':brand_products,
        'products':products_all,
        'wishlist_count':wishlist_count,
        'brand':brand,
        # 'categories':categories,
        # 'orderproducts': orderproducts
    }
    return render(request, 'vegefoods/index.html', context)





@login_required()
def addToWishlist(request, product_id, source):

    product = Product.objects.filter(id=product_id).first()
    buyer = Buyer.objects.filter(user_ptr_id=request.user.id).first()
    print(buyer)
    print(product)

    if buyer is not None and product is not None:
        Wishlist.objects.create(buyer=buyer, product=product)
        # messages.success(request, '')
        sweetify.success(request,  'Added successfully', timer=3000)
    else:
        # messages.error(request, '')
        sweetify.error(request, title='Error' 'Could not add product', button='ok', timer=5000)


    source = source.replace('____', '/')
    return redirect(source)


@login_required()
def unWishProduct(request, wishlist_id, source):
    buyer = Buyer.objects.filter(user_ptr_id=request.user.id).first()
    wishlist = Wishlist.objects.filter(id=wishlist_id)
    if buyer is not None:
        wishlist.delete()
        sweetify.success(request,  'Your Wish Have Been Removed', button='ok', timer=3000)
        # messages.success(request, '')
    source = source.replace('____', '/')
    return redirect(source)


@login_required()
def unWish_All_Products(request):
    buyer = Buyer.objects.filter(user_ptr_id=request.user.id).first()
    wishlist = Wishlist.objects.all().filter(buyer_id=request.user.id)
    if buyer is not None:

        wishlist.delete()
        sweetify.success(request,  'All Your Wishes Have Been Removed', button='ok', timer=3000)
        # messages.success(request, '')
    return redirect('Shoppy:shoppy-user_account')

# cart
login_required()
def cart(request):
    carts = Order_Product.objects.filter(buyer_id=request.user.id, checkout__isnull=True, product__wishlist__isnull=True)
    order_varianto = OrderProductVariantOption.objects.all()
    buyer =  Buyer.objects.filter(user_ptr_id=request.user.id).first()
    # variant =  Variant.objects.filter()
    # variant = Variant.objects.filter(variant_options__orderproductvariantoption__orderProduct_id=carts)
    # print(cart)
    context = {
        'carts' : carts,
        'title': 'Shoppy-Cart',
        'ordervarianto': order_varianto,
        'buyer':buyer,
        'carousels':Carousel.objects.all(),

    }
    return render(request, 'vegefoods/cart.html', context)

@login_required()
def addCart(request, product_id):

    product = Product.objects.filter(id=product_id).first()
    buyer = Buyer.objects.filter(user_ptr_id=request.user.id).first()

    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        unit_cost = request.POST.get('unit_cost')
        total = (float(unit_cost) * int(quantity))
        request.POST = request.POST.copy()
        # request.POST['total'] = total
        request.POST['buyer'] = buyer
        options = request.POST.getlist('variant_options[]')


        orderProduct = Order_Product.objects.create(
            product=product,
            buyer=buyer,
            quantity=quantity,
            total=total,
        )
        if options is not None:
            for variantoption in options:
                variant_option = Variant_Option.objects.filter(id=variantoption).first()
                OrderProductVariantOption.objects.create(
                    variantOptions=variant_option,
                    orderProduct=orderProduct,
                )
        sweetify.success(request,  'Product Added To Cart', button='ok', timer=3000)

        return redirect('Shoppy:shoppy-home')
    return redirect('Shoppy:shoppy-home')

def deleteCartProduct(request, order_id):
    cart_product = Order_Product.objects.filter(id=order_id).first()
    cart_product.delete()
    return redirect("Shoppy:shoppy-cart")


def productDetails(request, product_id):
    product = Product.objects.filter(id=product_id).first()
    images = Image.objects.filter(product= product_id)
    review_images = Image.objects.filter(product=product_id)[:2]
    reviews = Review.objects.filter(product=product).order_by('-created_at')
    product_carts = Product.objects.filter(id=product_id)
    similar_products= Product.objects.filter( product_brand=product.product_brand)
    buyer = Buyer.objects.filter(user_ptr_id=request.user.id).first()

    if request.method == 'POST':
        ratings = request.POST.get('ratings', False)
        comments = request.POST['comments']
        productt = request.POST['product']
        product = Product.objects.filter(id=productt).first()
        Review.objects.create(
            buyer=buyer,
            product=product,
            ratings=ratings,
            comments=comments,
        )
        sweetify.success(request, title='Success' 'Your Review Was Taken', button='ok', timer=3000)

    # sweetify.error(request, title='Error' 'You Can Only Review Products You Have Bought ', button='ok', timer=5000)


    context={
        'product' : product,
        'images' : images,
        'review_images': review_images,
        'similar_products':similar_products,
        'product_carts': product_carts,
        'reviews': reviews,
        'carousel':Carousel.objects.all()

    }

    return render(request, 'vegefoods/product-single.html',context)

def productsList(request, ):
    if request.method == "POST":
        category = request.POST.get('category')
        brand = request.POST.get('brand')
        unit_cost_from = request.POST.get('unit_cost_from')
        unit_cost_to = request.POST.get('unit_cost_to')

        filter_category = Category.objects.filter(id=category).first()
        filer_brand = Brand.objects.filter(id=brand).first()
        print(unit_cost_from, unit_cost_to, category, brand)
        if category is not None and brand is not None and unit_cost_from is not None and unit_cost_to is not None:
            products = Product.objects.filter(
                Q(category=filter_category) | Q(product_brand=filer_brand) | Q(status='VERIFIED') | Q(
                    unit_cost__range=[int(unit_cost_from), int(unit_cost_to)]))
            print('one')
            # print(products)

        elif category is not None and brand is not None:
            products = Product.objects.filter(Q(category=filter_category), Q(product_brand=filer_brand),
                                              Q(status='VERIFIED'),
                                              Q(unit_cost__range=[int(unit_cost_from), int(unit_cost_to)]))
            print('three')
            # print(products)
        elif brand is not None and unit_cost_from is not None and unit_cost_to is not None:
            products = Product.objects.filter(Q(product_brand=filer_brand), Q(status='VERIFIED'),
                                              Q(unit_cost__range=[int(unit_cost_from), int(unit_cost_to)]))
            print('four')
            # print(products)
        elif category is not None and unit_cost_from is not None and unit_cost_to is not None:
            products = Product.objects.filter(Q(category=filter_category), Q(status='VERIFIED'),
                                              Q(unit_cost__range=[int(unit_cost_from), int(unit_cost_to)]))
            print('five')
            # print(products)
        elif category is not None:
            products = Product.objects.filter(Q(category=filter_category), Q(status='VERIFIED'),
                                              Q(unit_cost__range=[int(unit_cost_from), int(unit_cost_to)]))
            print('six')
            # print(products)
        elif brand is not None:
            products = Product.objects.filter(Q(product_brand=filer_brand), Q(status='VERIFIED'),
                                              Q(unit_cost__range=[int(unit_cost_from), int(unit_cost_to)]))
            print('seven')
            # print(products)
        elif unit_cost_to is not None and unit_cost_from is not None:
            products = Product.objects.filter(Q(status='VERIFIED'),
                                              Q(unit_cost__range=[int(unit_cost_from), int(unit_cost_to)]))
            print('two')
            # print(products)

        max_cost = Product.objects.order_by('-unit_cost').values('unit_cost').first()['unit_cost']
        # print(products)
        context = {
            'products': products,
            'categories': Category.objects.filter(parent_id__isnull=True).order_by('name'),
            'brands': Brand.objects.all(),
            'max_cost': int(max_cost),
            'min_cost': 0,

        }
        # return TemplateResponse(request, "shoppy/view_products/filtered_products.html", context)
        # return render_to_response('shoppy/view_products/filtered_products.html',context)
        return render(request, 'shoppy/view_products/all_category_products.html', context)

    else:
        products = Product.objects.filter(status='VERIFIED').order_by('-unit_cost')
        context = {
            'products': products,
            'categories': Category.objects.all(),
            'brands': Brand.objects.all(),
            'max_cost': int(Product.objects.order_by('-unit_cost').values('unit_cost').first()['unit_cost']),
            'min_cost': 0,
            'carousels':Carousel.objects.all(),

        }

    return render(request, 'vegefoods/shop.html', context)




# def productReview(request):
#     buyer = Buyer.objects.filter(user_ptr_id=request.user.id).first()
#     if buyer is not None:
#         if request.method == 'POST':
#             ratings = request.POST.get('ratings', False)
#             comments = request.POST['comments']
#             productt = request.POST['product']
#             product = Product.objects.filter(id=productt).first()
#             Review.objects.create(
#                 buyer=buyer,
#                 product=product,
#                 ratings=ratings,
#                 comments=comments,
#             )
#             sweetify.success(request, title='Success' 'Your Review Was Taken', button='ok', timer=3000)
#             return redirect("Shoppy:shoppy_product_details")
#     sweetify.error(request, title='Error' 'You Can Only Review Products You Have Bought ', button='ok', timer=5000)
#     return redirect("Shoppy:shoppy_product_details")

# def user_account_product(request, product_id):
#     similar =Product.objects.filter(id=product_id).first()
#     product = Product.objects.filter(product_brand=similar.product_brand)
#     context={
#         'product':product,
#     }
#     return render(request, 'shoppy/user_account.html', context)
login_required()
def wishlist(request):
    user = request.user
    buyer = Buyer.objects.filter(user_ptr_id=user.id).first()


    wishlist = Wishlist.objects.filter(buyer_id=request.user.id)
    context = {
        # 'user': logged_in_user,
        'wishlist': wishlist,
        'carousels':Carousel.objects.all(),
        'orders': Order_Product.objects.filter(buyer=buyer, checkout__isnull=False, checkout__status='PAID'),
        'buyer': Buyer.objects.filter(user_ptr_id=user.id).first(),
    }
    return render(request, 'vegefoods/wishlist.html', context)
@login_required()
def user_account(request):
    user = request.user
    buyer = Buyer.objects.filter(user_ptr_id=user.id).first()
    seller = Seller.objects.filter(user_ptr_id=user.id).first()
    wishlist = Wishlist.objects.filter(buyer_id=request.user.id)


    if buyer is not None:
        logged_in_user = 'buyer'
    elif seller is not None:
        logged_in_user = 'seller'

    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone_number = request.POST['phone_number']
        if buyer is not None:
            user = User.objects.get(pk=request.user.id)
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.save()
            Buyer.objects.filter(user_ptr_id = user.id).update(
                phone_number = phone_number,
            )
            sweetify.success(request, title='Success' 'Account Updated', button='ok', timer=5000)
    context ={
        'user': logged_in_user,
        'wishlist': wishlist,
        'orders':Order_Product.objects.filter(buyer=buyer, checkout__isnull=False , checkout__status='PAID'),
        'buyer' : Buyer.objects.filter(user_ptr_id=user.id).first(),
    }
    return render(request,'shoppy/user_account.html',context)




def buyer_register(request):
    # user= request.user

    if request.method == 'POST':
        username =request.POST['username']
        form = BuyerSignUpForm(request.POST)
        print(form)
        if form.is_valid():
            new_form = form.save()
            # user = User.objects.filter(id=n)
            Buyer.objects.filter(user_ptr_id=new_form.id).update(
                phone_number = username,
            )
            sweetify.success(request, 'Buyer Registered Successfully, Now Log In', persistent='Continue', timer=3000)
            return redirect('Shoppy:shoppy-login')
        else:
            form1 = BuyerSignUpForm(request.POST)
            sweetify.error(request, 'Error', text='Ensure you fill all fields correctly', persistent='Retry', timer=3000)
            return render(request,"vegefoods/loginorregister.html", {
                'form':form1,
                'carousels': Carousel.objects.all()
            })
    else:
        form2 = BuyerSignUpForm()
    context={
        'form': form2,
        'carousels':Carousel.objects.all()
    }
    return  render(request,"vegefoods/loginorregister.html",context)
    # return redirect('Shoppy:shoppy-buyer-reg',context)


def user_login(request):
    # messages = []
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']


        def buyerusername(phone_number):
            uz= Buyer.objects.filter(Q(phone_number__exact=username)|Q(username__exact=username)).first()
            usename = User.objects.filter(id=uz.user_ptr_id).first()
            if uz.phone_number:
                return usename.username
            return None
        def sellerusername(email):
            # uz = User.objects.filter(email__exact=email).first()
            uz= Seller.objects.filter(Q(email__exact=email) | Q(username__exact=email)).first()
            usename = User.objects.filter(id=uz.id).first()
            if uz.email:
                return usename.username
            return None
        def adminusername(username):
            uzer=User.objects.filter(Q(username__exact=username) | Q(email__exact=username)).first()
            if uzer:
                return uzer.username
            return None




        if  User.objects.filter(Q(username__exact=username) | Q(email__exact=username)).first() or \
            Buyer.objects.filter(phone_number__exact=username).first() or \
            Seller.objects.filter(Q(email__exact=username) | Q(username__exact=username)).first():
            if Buyer.objects.filter(Q(phone_number__exact=username) | Q(username__exact=username)).first():
                user = authenticate(username=buyerusername(username), password=password)
                if user is not None:
                    if user.is_active:
                        if Buyer.objects.filter(user_ptr_id=user.id).exists():
                            login(request, user)
                            sweetify.success(request, 'Success', text='Welcome to Jikonify', persistent='Continue')
                            return redirect('Shoppy:shoppy-home')
                    else:
                        sweetify.error(request, 'Error', text='Your account has been Deactivated!',
                                       persistent='Retry')
                        return render(request, 'vegefoods/loginorregister.html')
                else:
                    sweetify.error(request, 'Error', text='Invalid login credentials', persistent='Retry')
                    return render(request, 'vegefoods/loginorregister.html')
            if Seller.objects.filter(Q(email__exact=username) | Q(username__exact=username)).first():
                user = authenticate(username=sellerusername(username), password=password)
                if user is not None:
                    if user.is_active:
                        if Seller.objects.filter(user_ptr_id=user.id).exists():
                            if Seller.objects.filter(user_ptr_id=user.id, status="VERIFIED").exists():
                                login(request, user)
                                sweetify.success(request, 'Success', text='Welcome to Jikonify', persistent='Retry')
                                return redirect('ShoppyAdmin:shoppy-admin-home')
                            else:
                                sweetify.error(request, 'Error',
                                               text='It Seems That Your Account Has Been Deactivated: Contact The Admin For More Info',
                                               persistent='Retry')
                                return render(request, 'vegefoods/loginorregister.html')
                    else:
                        sweetify.error(request, 'Error', text='Your account has been Deactivated!',
                                       persistent='Retry')
                        return render(request, 'vegefoods/loginorregister.html')
                else:
                    sweetify.error(request, 'Error', text='Invalid login credentials', persistent='Retry')
                    return render(request, 'vegefoods/loginorregister.html')
            if User.objects.filter(Q(username__exact=username)|Q(email__exact=username) and Q(is_superuser=True)).first():
                user = authenticate(username=adminusername(username), password=password,)
                if user is not None:
                    if user.is_staff and user.is_active:
                        login(request, user)
                        sweetify.success(request, 'Success', text='Welcome Admin',persistent='Continue')
                        return redirect('ShoppyAdmin:shoppy-admin-home')
                    else:
                        sweetify.error(request, 'Error', text='Please Retry', persistent='Retry')
                        return render(request, 'vegefoods/loginorregister.html')
                else:
                    sweetify.error(request, 'Error', text='Invalid login credentials', persistent='Retry')
                    return render(request, 'vegefoods/loginorregister.html')

        else:

            sweetify.error(request, 'Error', text='Invalid user credentials', persistent='Continue')
    context={
        'carousels': Carousel.objects.all()
    }
    return render(request,"vegefoods/loginorregister.html", context)



def logout_view(request):
    logout(request)
    return redirect('Shoppy:shoppy-login')

def seller_register(request):

    if request.method == 'POST':
        form = SellerSignUpForm(request.POST, request.FILES)
        # print(form)
        if form.is_valid():
            form.save()
            sweetify.success(request, 'Success', text='Seller Registered Successfully, You Will Be Notified When Your Account Is Activated', persistent='Continue')
            return redirect('Shoppy:shoppy-login')
        else:
            form = SellerSignUpForm(request.POST, request.FILES)
            sweetify.error(request, 'Error', text='Error Registering, ensure all your details are field correctly', persistent='Retry')
            # return redirect('shoppy/seller_registration.html')
            return render(request,'shoppy/seller_registration.html',{'form':form,'counties': County.objects.order_by('-number'),})

    # kenyan_county_api_url = "https://raw.githubusercontent.com/mikelmaron/kenya-election-data/master/data/counties.geojson"
    # data = requests.get(kenyan_county_api_url).json()
    #
    # for county in data['features']:
    #     County.objects.create(
    #         name=county['properties']['COUNTY_NAM'],
    #         number=county['properties']['COUNTY_COD'],
    #     )
    context = {
        'counties': County.objects.order_by('-number'),
    }

    return render(request, 'shoppy/seller_registration.html', context)


# def seller_home(request):
#     user = request.user
#     seller = Seller.objects.filter(user_ptr_id=user.id).first()
#     return render(request, 'shoppy_seller/sellerhome.html', {'seller':seller})

def checkout(request):
    buyer = Buyer.objects.filter(user_ptr_id=request.user.id).first()
    # print(buyer.)
    regions= Region.objects.all()
    carts = Order_Product.objects.filter(buyer_id=buyer.id ,checkout__isnull=True, product__wishlist__isnull=True)

    # print(buyer)
    context={
        'buyer':buyer,
        'regions': regions,
        'carts':carts,
        'carousels':Carousel.objects.all()
    }
    return render(request, 'vegefoods/checkout.html', context)

def confirmCheckout(request):
    buyer = Buyer.objects.filter(user_ptr_id=request.user.id).first()
    if request.method =="POST":
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        total=request.POST['total']
        phonenumber= request.POST['phone_number']
        reference_code =('M'+ get_random_string(length=4, allowed_chars='ABCDEFGHIJLNPQRSTUVWXYZ123456789'))

        if not User.objects.filter(id=request.user.id, last_name__iexact=last_name, first_name__iexact=first_name).exists():
            User.objects.filter(id = request.user.id).update(
                first_name=first_name,
                last_name=last_name,
            )
        checkout = Checkout.objects.create(
            buyer=buyer,
            reference_code = reference_code,
            total = float(total),
            phonenumber = phonenumber
        )
        if checkout is not None:
            checkoutt = Checkout.objects.filter(id=int(checkout.id)).first()
            buyerr = Buyer.objects.filter(user_ptr_id=request.user.id).first()
            Order_Product.objects.filter(buyer=buyerr, checkout__isnull=True).update(
                buyer=buyer,
                checkout=checkoutt,
            )
            new_orders = Order_Product.objects.filter(checkout=checkoutt)


            try:
                orders_products = []
                for order in new_orders:
                    orders_products.append(order.product.name)
                # username = "Mashkys"    # use 'sandbox' for development in the test environment
                username = "eugenewere"  # use 'sandbox' for development in the test environment
                api_key = "495ade1667cabcfa21092603ff76876cd2bc01371d7e08252dc45a8c1a1b5103"  # use your sandbox app API key for development in the test environment
                # api_key = "652230d338f11fd49333722a8acba0161942b5b3efb880caf2fb21958e4fdde4"      # use your sandbox app API key for development in the test environment
                africastalking.initialize(username, api_key)

                phonenumberr = buyerr.phone_number
                # appKey = request.data.get("appSignature")
                new_phone_number = f"{254}{phonenumberr[-9:]}"

                sms = africastalking.SMS
                # Use the service synchronously
                # response = sms.send("<#> Your Orders are: " + str(", ".join( repr(e) for e in orders_products ) ) +'. We will call you to confirm the order', ["+" + new_phone_number], )
                # print(response)
                context = {
                    'results': 'success',
                    'response': "We have text you pin for setting your password, if an account exists with the phonenumber you entered You should receive an SMS shortly. If you don't receive an email, please make sure you've entered the phonenumber you registered with "

                }
                sweetify.success(request, title='Success' 'Check your phone for order details', button='ok')
            except:
                print('NO INTERNET')
                context = {
                    'results': 'error',
                    'response': "No Internet "

                }

        sweetify.success(request, title='Success' 'Order Taken You Will Be Notified If Its Ready', button='Continue', timer=5000)
        return redirect("Shoppy:how_to_pay")
    else:
        sweetify.error(request, title='Error' 'Error taking your order', button='Retry', timer=5000)

    return redirect("Shoppy:how_to_pay")

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            sweetify.success(request, title='Sucess' 'Your password was successfully updated!', button='ok', timer=5000)
            # messages.success(request, '')
            return redirect('Shoppy:shoppy-user_account')
        else:
            sweetify.error(request, title='Error' 'Please correct the error in the form', button='ok', timer=5000)
            # messages.error(request, '')
    else:
        form = PasswordChangeForm(request.user)

    return render(request,'shoppy/user_account.html', {
        'form': form
    })





def how_to_pay(request):
    user = request.user.id
    buyer = Buyer.objects.filter(user_ptr_id=user).first()
    checkout_id = Checkout.objects.filter(buyer=buyer).order_by('-id').first()
    order_total =  Order_Product.objects.filter(buyer=buyer, checkout_id__exact=checkout_id )

    context={
        'order_total':order_total,
        'checkout':checkout_id,
        'carousels':Carousel.objects.all()
    }
    return render(request,'vegefoods/howtopay.html',context)


def product_filter(request):
    if request.method == "POST":
        category = request.POST.get('category')
        brand = request.POST.get('brand')
        unit_cost = request.POST['unit_cost']
        filter_category = Category.objects.filter(id=category).first()
        filer_brand = Brand.objects.filter(id=brand).first()
        print(unit_cost)
        if category and brand and unit_cost:
            products = Product.objects.filter(Q(category=filter_category), Q(product_brand=filer_brand), Q(status='VERIFIED') , unit_cost__gte=0, unit_cost__lt=unit_cost)
            # products = Product.objects.filter(Q(category=filter_category), Q(product_brand=filer_brand), Q(unit_cost__range=[0, float(unit_cost)]), Q(status='VERIFIED'))
        elif category:
            products = Product.objects.filter(Q(category=filter_category), Q(status='VERIFIED'))
        elif brand:
            products = Product.objects.filter(Q(product_brand=filer_brand), Q(status='VERIFIED'))
        elif unit_cost:
            products = Product.objects.filter(  Q(status='VERIFIED'), unit_cost__gte=0, unit_cost__lt=unit_cost)
            # products = Product.objects.filter( Q(unit_cost__range=[0, float(unit_cost)]), Q(status='VERIFIED'))



        max_cost = Product.objects.order_by('-unit_cost')[0]
        context = {
            'products': products,
            'categories': Category.objects.all(),
            'brands': Brand.objects.all(),
            'max_cost':max_cost,

        }
        return render(request, 'shoppy/view_products/all_products.html', context)

    else:
        products = Product.objects.filter(status='VERIFIED')
        context={
            'products':products,
            'categories': Category.objects.all(),
            'brands': Brand.objects.all(),

        }
        return render(request, 'shoppy/view_products/all_products.html', context)

def getShortcode(request):
    # Initialize SDK
    if request.method == 'POST':
        try:
            # username = "Mashkys"    # use 'sandbox' for development in the test environment
            username = "eugenewere"  # use 'sandbox' for development in the test environment
            api_key = "495ade1667cabcfa21092603ff76876cd2bc01371d7e08252dc45a8c1a1b5103"  # use your sandbox app API key for development in the test environment
            # api_key = "652230d338f11fd49333722a8acba0161942b5b3efb880caf2fb21958e4fdde4"      # use your sandbox app API key for development in the test environment
            africastalking.initialize(username, api_key)
            random_code = get_random_string(length=6, allowed_chars='123456789')
            phonenumber = request.POST.get("phone_number")
            # appKey = request.data.get("appSignature")
            new_phone_number = f"{254}{phonenumber[-9:]}"
            # print(new_phone_number)
            short_code = ShortCode.objects.create(

                phone_number=phonenumber,
                short_code=random_code,
            )
            # Initialize a service e.g. SMS
            sms = africastalking.SMS
            # Use the service synchronously
            response = sms.send("<#> Your JIKONIFY code is:" + random_code, ["+" + new_phone_number],)
            context = {
                'results': 'success',
                'response': "We have text you pin for setting your password, if an account exists with the phonenumber you entered You should receive an SMS shortly. If you don't receive an email, please make sure you've entered the phonenumber you registered with "

            }
            # sweetify.success(request, title='Success' 'Check your phone for a code we have sent to your and key it into the number pad below. ', button='ok')
        except:
            # print('NO INTERNET')
            context = {
                'results': 'error',
                'response': "No Internet "

            }

        return JsonResponse(context, safe=False)
    # return render(request, 'shoppy/registration/password_reset_done.html', context)

def password_resett(request):
    return render(request, 'shoppy/registration/password_reset.html')


def pin_confirmm(request):
    return render(request, 'shoppy/registration/password_reset_done.html')
def new_pin(request):

    return render(request, 'shoppy/registration/password_reset_confirm.html')

def verifyCode(request):
    if request.method == 'POST':
        short_code = request.POST.get("short_code")
        db_short_code = ShortCode.objects.filter(short_code=short_code).order_by('-created_at')[0]
        phoneno = db_short_code.phone_number
        if ShortCode.objects.filter(phone_number = phoneno, short_code = short_code).exists():
           print(db_short_code)
           db_short_code.delete()
           # sweetify.success(request, title='Success' 'Change your pin now!. ',
           #                  button='ok', timer=5000)

           # redirect('Shoppy:new_pin',title='Success' 'Change your pin now!. ',
           #                  button='ok', timer=5000)
           context = {
               'results': 'success',
               'response': 'Change your pin now',
               'phone_number': phoneno,
           }
           return JsonResponse(context, safe=False)

        else:
            print('error')
            context = {
                'results': 'error',
                'response': 'Wrong Short Code Please Retry'
            }
            return JsonResponse(context, safe=False)
    context = {
        'response': 'Wrong Short Code'
    }
    return JsonResponse(context, safe=False)

def verifypassword(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:
            u = User.objects.get(username__exact=phone_number)
            u.set_password(password1)
            u.save()
            context = {
                'results':'success',
                'response': 'You have successfuly changed your pin. You can log in Now'
            }
            return JsonResponse(context, safe=False)
        else:
            context = {
                'results':'error',
                'response': 'Pin dont match'
            }
            return JsonResponse(context, safe=False)

    context = {
        'response': ''
    }
    return JsonResponse(context, safe=False)
def deleteme(request):
    user = request.user
    carousels = Carousel.objects.order_by("-created_at")
    brand = Brand.objects.order_by('?').first()
    products = Product.objects.order_by("?")
    featured_products = Product.objects.filter(feat_product='FEATURED', status='VERIFIED')
    products_all = Product.objects.filter(status='VERIFIED').order_by('?')
    wishlist_count = Wishlist.objects.filter(buyer_id=request.user.id).count()

    context = {
        'title': 'Shoppy-Home',
        'user': user,
        'carousels': carousels,
        'featured_products': featured_products,
        # 'products': products,
        'products': products_all,
        'wishlist_count': wishlist_count,
        # 'brand':brand,
        # 'categories':categories,
        # 'orderproducts': orderproducts
    }
    return render(request, 'shoppy/deleteme.html', context)