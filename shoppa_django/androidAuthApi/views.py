from django_project import settings
from shoppy.models import Buyer, Category, Product, Order_Product, Wishlist, Checkout, Region, Product_Variant_Options, \
    NewsLetter, CheckoutPayment
from shoppy.models import Variant_Option, Variant, Carousel, Review, Image, OrderProductVariantOption, Brand, Offer
from .serializers import buyersSerializer, CategorySerializer, ProductSerializer, OrderProductSerializer, ParentVariantSerializer
from .serializers import  AllProductsSerializer, AndroidProductSerializer, CustomCartSerializer, wishlistSerializer, CustomWishlistSerializer
from .serializers import RegionSerializer, CheckoutSerializer, VariantOptionsSerializer, CustomVariantsSerializer, VariantsSerializer
from .serializers import CarouselSerializer, ReviewSerializer, ImageSerializer, CartVariantSerializer
from .models import ShortCode
from rest_framework import generics
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_201_CREATED
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, FloatField, IntegerField, CharField, Value, DateTimeField, Q
from django.utils.crypto import get_random_string
import africastalking


# from django.http import HttpResponse
# from django.shortcuts import get_object_or_404


class UserList(generics.ListAPIView):
    queryset = Buyer.objects.all()
    serializer_class = buyersSerializer
    permission_classes = [IsAuthenticated]

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Buyer.objects.all()
    serializer_class = buyersSerializer

class CategoryList(generics.ListAPIView):
    queryset = Category.objects.filter(parent_id__isnull=True)
    serializer_class = CategorySerializer

class UnfilteredCategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class AllProductList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = AllProductsSerializer


class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class WishList(generics.ListAPIView):
    queryset = Wishlist.objects.all()
    serializer_class = wishlistSerializer

class RegionList(generics.ListAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer

class RegionList(generics.ListAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer    
 

class ProductDetails(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class RegionDetails(generics.ListAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer

    # def get_queryset(self):
    #     category = self.kwargs['category']
    #     if category is not None:
    #         return Product.objects.filter(brand= category)
    #     else:
    #         return Product.objects.all()

class OrderProductList(generics.ListAPIView):
    queryset = Order_Product.objects.all()
    serializer_class = OrderProductSerializer

class VariantOptionList(generics.ListAPIView):
    queryset = Product_Variant_Options.objects.all()
    serializer_class = VariantOptionsSerializer

class ReviewList(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class CarouselAdverts(generics.ListAPIView):
    queryset = Carousel.objects.all()
    serializer_class = CarouselSerializer    
 
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def signup2(request):
    username = request.data.get("username", "")
    password = request.data.get("password", "")
    email = request.data.get("email", "")
    first_name = request.data.get("first_name", "")
    last_name = request.data.get("last_name", "")
    phone_number = request.data.get("phone_number", "")
    if not username and not password and not email and not first_name and not last_name:
        return Response(
            data={
                "message": "username, password and email is required to register a user"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    new_buyer = Buyer.objects.create_user(
        # user_ptr_id=new_buyer.id,
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name,
        phone_number=phone_number,
        is_staff=False
    )
    context = {
        'message': 'You Have Been Successfully Registered'
    }
    return Response(context,status=status.HTTP_201_CREATED)

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    phonenumber = request.data.get("username")
    password = request.data.get("password")

    buyer = Buyer.objects.filter(Q(phone_number = phonenumber)| Q(username__exact=phonenumber)).first()
    if buyer:
        username = buyer.username
        if username is None or password is None:
            return Response({'error': 'Please provide both username and password'}, status=HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)

        if not user:
            context = {
                'error': 'Invalid Username or Password',
            }
            return Response(context, status=HTTP_404_NOT_FOUND)
        token, _ = Token.objects.get_or_create(user=user)
        context = {
            'token': token.key,
            'id': user.id,
            'username': username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name
        }
        return Response(context,
                        status=HTTP_200_OK)
    else:
        return Response({'error': 'Only Buyers are allowed to login'}, status=HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def addtocart(request, product_id):
    # print(request.META['HTTP_AUTHORIZATION'])
    r_token = request.META['HTTP_AUTHORIZATION']
    new_token = r_token.split(' ', 1)[1]

    product = Product.objects.filter(id=product_id).first()
    token = Token.objects.filter(key=new_token).first()
    buyer = Buyer.objects.filter(user_ptr_id=token.user.id).first()
    quantity = request.data.get("quantity")
    if not product_id and not quantity:
        return Response(
            data={
                "Message": "Make Sure All The Fields Are Included"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    if Order_Product.objects.filter(buyer = buyer, product = product, checkout__isnull = True).exists():
        return Response(
            data={
                "Message": "Product Already In Cart"
            },
            status = status.HTTP_400_BAD_REQUEST
        )
    offer = Offer.objects.filter(product = product).first()
    if offer is not None:
        amount = offer.discount
    else:
        amount = product.unit_cost

    new_OrderProduct = Order_Product.objects.create(
        product=product,
        buyer=buyer,
        quantity=quantity,
        total=(float(amount)*float(quantity)),
    )
    products = []
    r_token = request.META['HTTP_AUTHORIZATION']
    new_token = r_token.split(' ', 1)[1]
    token = Token.objects.filter(key=new_token).first()
    buyer = Buyer.objects.filter(user_ptr_id=token.user.id).first()
    cart_items = Order_Product.objects.filter(buyer=buyer, checkout__isnull=True)
    for order in cart_items:
        if order.quantity is not None:
            print(order.quantity)
            product = Product.objects.filter(id=order.product.id).annotate(order_id=Sum(order.id, output_field=IntegerField()),quantity=Sum(order.quantity, output_field=FloatField()), total=Sum(order.total, output_field=FloatField())).first()
            print(product.quantity)
            products.append(product)
    data = CustomCartSerializer(products, many=True)    
    context = {
        'data': data.data
    }

    return Response(data.data, status=status.HTTP_201_CREATED)


@csrf_exempt
@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def addCartVariant(request, order_id):
    variants = request.data.get("stringPojo")
    variant = Variant_Option.objects.filter(name = variants).first()
    cartProduct = Order_Product.objects.filter(id = order_id).first()
    new_OrderProductVariant = OrderProductVariantOption.objects.create(
        orderProduct = cartProduct,
        variantOptions = variant,
    )
    context = {
        'response': 'success'
    }
    return Response(data={
                "Message": "Success"
            }, status=status.HTTP_200_OK)

@csrf_exempt
@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def getCartVariant(request, order_id):
    variants = []
    print(order_id)
    cart = Order_Product.objects.filter(id = order_id).first()
    orderProductVariant = OrderProductVariantOption.objects.filter(orderProduct = cart)
    for order in orderProductVariant:
        variant = Variant_Option.objects.filter(id = order.variantOptions.id).first()
        variants.append(variant)
    data = VariantsSerializer(variants, many= True)
    context = {
        'data': data.data
    }
    return Response(data.data, status=status.HTTP_200_OK) 
    

@csrf_exempt
@api_view(["DELETE"])
@permission_classes((IsAuthenticated,))
def removefromcart(request, order_id):
    cart_product = Order_Product.objects.filter(id=order_id).first()
    cart_variant = OrderProductVariantOption.objects.filter(orderProduct = cart_product)
    for variant in cart_variant:
        variant.delete()
    cart_product.delete()
    products = []
    r_token = request.META['HTTP_AUTHORIZATION']
    new_token = r_token.split(' ', 1)[1]
    token = Token.objects.filter(key=new_token).first()
    buyer = Buyer.objects.filter(user_ptr_id=token.user.id).first()
    cart_items = Order_Product.objects.filter(buyer=buyer, checkout__isnull=True)
    for order in cart_items:
        if order.quantity is not None:
            print(order.quantity)
            product = Product.objects.filter(id=order.product.id).annotate(order_id=Sum(order.id, output_field=IntegerField()),quantity=Sum(order.quantity, output_field=FloatField()), total=Sum(order.total, output_field=FloatField())).first()
            print(product.quantity)
            products.append(product)
    data = CustomCartSerializer(products, many=True)    
    context = {
        'data': data.data
    }

    return Response(data.data,status=status.HTTP_201_CREATED)

@csrf_exempt
@api_view(["PUT"])
@permission_classes((IsAuthenticated,))
def updatecart(request, order_id):
    print(order_id)
    current_orderproduct = Order_Product.objects.filter(id = order_id).first()
    quantity = request.data.get("quantity",)
    product = Product.objects.filter(id =current_orderproduct.product.id).first()
    amount = product.unit_cost
    if not quantity:
        return Response(
            data={
                "Message": "Make Sure All The Fields Are Included"
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    current_orderproduct.quantity = quantity
    current_orderproduct.total = float(amount)*float(quantity)
    current_orderproduct.save()
 
    products = []
    r_token = request.META['HTTP_AUTHORIZATION']
    new_token = r_token.split(' ', 1)[1]
    token = Token.objects.filter(key=new_token).first()
    buyer = Buyer.objects.filter(user_ptr_id=token.user.id).first()
    cart_items = Order_Product.objects.filter(buyer=buyer, checkout__isnull=True)
    for order in cart_items:
        if order.quantity is not None:
            print(order.quantity)
            product = Product.objects.filter(id=order.product.id).annotate(order_id=Sum(order.id, output_field=IntegerField()),quantity=Sum(order.quantity, output_field=FloatField()), total=Sum(order.total, output_field=FloatField())).first()
            print(product.quantity)
            products.append(product)
    data = CustomCartSerializer(products, many=True)    
    context = {
        'data': data.data
    }

    return Response(data.data,status=status.HTTP_200_OK)

@csrf_exempt
@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def getcartproducts(request):
    products = []
    r_token = request.META['HTTP_AUTHORIZATION']
    new_token = r_token.split(' ', 1)[1]
    token = Token.objects.filter(key=new_token).first()
    buyer = Buyer.objects.filter(user_ptr_id=token.user.id).first()
    cart_items = Order_Product.objects.filter(buyer=buyer, checkout__isnull=True)
    for order in cart_items:
        if order.quantity is not None:
            print(order.quantity)
            product = Product.objects.filter(id=order.product.id).annotate(order_id=Sum(order.id, output_field=IntegerField()),quantity=Sum(order.quantity, output_field=FloatField()), total=Sum(order.total, output_field=FloatField())).first()
            print(product.quantity)
            products.append(product)
    data = CustomCartSerializer(products, many=True)    
    context = {
        'data': data.data
    }

    return Response(data.data,status=status.HTTP_200_OK)

@csrf_exempt
@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def getPendingPaymentProducts(request, checkout_id):
    products = []
    r_token = request.META['HTTP_AUTHORIZATION']
    new_token = r_token.split(' ', 1)[1]
    token = Token.objects.filter(key=new_token).first()
    buyer = Buyer.objects.filter(user_ptr_id=token.user.id).first()
    cart_items = Order_Product.objects.filter(buyer=buyer, checkout = checkout_id )
    for order in cart_items:
        product = Product.objects.filter(id=order.product.id).first()
        products.append(product)
    data = ProductSerializer(products, many=True)    
    context = {
        'data': data.data
    }

    return Response(data.data,status=status.HTTP_200_OK)


@csrf_exempt
@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def getBuyerOrderHistory(request,):
    r_token = request.META['HTTP_AUTHORIZATION']
    new_token = r_token.split(' ', 1)[1]
    token = Token.objects.filter(key=new_token).first()
    buyer = Buyer.objects.filter(user_ptr_id=token.user.id).first()
    orders = Checkout.objects.filter(buyer = buyer)
    data = CheckoutSerializer(orders, many=True)    
    context = {
        'data': data.data
    }

    return Response(data.data,status=status.HTTP_200_OK)        


@csrf_exempt
@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def addtowishlist(request, product_id):
    # print(request.META['HTTP_AUTHORIZATION'])
    products = []
    r_token = request.META['HTTP_AUTHORIZATION']
    new_token = r_token.split(' ', 1)[1]
    product = Product.objects.filter(id=product_id).first()
    token = Token.objects.filter(key=new_token).first()
    buyer = Buyer.objects.filter(user_ptr_id=token.user.id).first()
    if not product_id:
        return Response(
            data={
                "Message": "Product does not exist"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    if Wishlist.objects.filter(buyer = buyer, product = product).exists():
        return Response(
            data={
                "Message": "Product already in wishlist"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    new_wishlistProduct = Wishlist.objects.create(
        product=product,
        buyer=buyer,
    )

    productID = Wishlist.objects.filter(buyer=buyer)
    for order in productID:
        Wishlist_product = Product.objects.filter(id = order.product.id).annotate(wishlist_id=Sum(order.id, output_field=IntegerField())).first()
        products.append(Wishlist_product)
    data = CustomWishlistSerializer(products, many=True)    
    context = {
        'data': data.data
    }
    return Response(data.data,status=status.HTTP_201_CREATED)

@csrf_exempt
@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def getwishlistproducts(request):
    # print(request.META['HTTP_AUTHORIZATION'])
    products = []
    r_token = request.META['HTTP_AUTHORIZATION']
    new_token = r_token.split(' ', 1)[1]
    token = Token.objects.filter(key=new_token).first()
    buyer = Buyer.objects.filter(user_ptr_id=token.user.id).first()
    if not buyer:
        return Response(
            data={
                "Message": "You are not logged in"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    wishlistProducts = Wishlist.objects.filter(buyer=buyer)
    for order in wishlistProducts:
        allwishlistproducts = Product.objects.filter(id = order.product.id).annotate(wishlist_id=Sum(order.id, output_field=IntegerField())).first()
        products.append(allwishlistproducts)
    data = CustomWishlistSerializer(products, many=True)    
    context = {
        'data': data.data
    }

    return Response(data.data,status=status.HTTP_200_OK)

@csrf_exempt
@api_view(["DELETE"])
@permission_classes((IsAuthenticated,))
def removefromwishlist(request, wishlist_id):
    products = []
    wishlist_product = Wishlist.objects.filter(id=wishlist_id).first()
    wishlist_product.delete()
    products = []
    r_token = request.META['HTTP_AUTHORIZATION']
    new_token = r_token.split(' ', 1)[1]
    token = Token.objects.filter(key=new_token).first()
    buyer = Buyer.objects.filter(user_ptr_id=token.user.id).first()
    if not buyer:
        return Response(
            data={
                "Message": "You are not logged in"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    wishlistProducts = Wishlist.objects.filter(buyer=buyer)
    for order in wishlistProducts:
        allwishlistproducts = Product.objects.filter(id = order.product.id).annotate(wishlist_id=Sum(order.id, output_field=IntegerField())).first()
        products.append(allwishlistproducts)
    data = CustomWishlistSerializer(products, many=True)    
    context = {
        'data': data.data
    }

    return Response(data.data,status=status.HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def getproducts(request):
    category = request.data.get("name")
    print(category)
    categories = Category.objects.filter(name = category).first()
    products = Product.objects.filter(category=categories.id, status = 'VERIFIED')
    data = ProductSerializer(products, many = True)
    context = {
        'data': data.data
    }

    return Response(data.data,status=status.HTTP_200_OK)

@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def getProductsFromCategoryId(request, category_id):
    categories = Category.objects.filter(id = category_id).first()
    products = Product.objects.filter(category=categories.id, status = 'VERIFIED')
    data = ProductSerializer(products, many = True)
    context = {
        'data': data.data
    }

    return Response(data.data,status=status.HTTP_200_OK)

@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def getProductImages(request, product_id):
    images = Image.objects.filter(product=product_id)
    data = ImageSerializer(images, many = True)
    context = {
        'data': data.data
    }

    return Response(data.data,status=status.HTTP_200_OK)

@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def getSpecificProduct(request, product_id):
    products = Product.objects.filter(id=product_id, status = 'VERIFIED')
    data = ProductSerializer(products, many = True)
    context = {
        'data': data.data
    }

    return Response(data.data,status=status.HTTP_200_OK)        

@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def getfeaturedproducts(request):
    products = Product.objects.filter(feat_product = 'FEATURED')
    data = ProductSerializer(products, many = True)
    context = {
        'data': data.data
    }

    return Response(data.data,status=status.HTTP_200_OK)

@csrf_exempt
@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def checkout(request):
    print(request.data)
    r_token = request.META['HTTP_AUTHORIZATION']
    new_token = r_token.split(' ', 1)[1]
    token = Token.objects.filter(key=new_token).first()
    buyer = Buyer.objects.filter(user_ptr_id=token.user.id).first()

    total = request.data.get("quantity")
    payment = request.data.get("payment")
    region_id = request.data.get("region_id")
    delivery_address = request.data.get("delivery_address")

    region = Region.objects.filter(id=region_id).first()
    newtotal = (float(total) + region.region_cost)

    new_checkoutorder = Checkout.objects.create(
        buyer = buyer,
        phonenumber = buyer.phone_number,
        total = newtotal,
        reference_code = "M"+ get_random_string(length=4, allowed_chars='123456789ABCDEFGHIJKLMNPQRSTUVWXYZ'),
        status = "PENDING",
        paymentchoice=payment,
        region=region,
        address=delivery_address,

    )
    cart_items = Order_Product.objects.filter(buyer=buyer, checkout__isnull=True).update(
        checkout = new_checkoutorder.id
    )
    # checkouts = Checkout.objects.filter(id = new_checkoutorder.id).first()
    checkoutt = Checkout.objects.filter(id=int(new_checkoutorder.id)).first()
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

        phonenumberr = buyer.phone_number
        # appKey = request.data.get("appSignature")
        new_phone_number = f"{254}{phonenumberr[-9:]}"

        sms = africastalking.SMS
        # Use the service synchronously
        response = sms.send("<#> Your Orders are: " + str(
            ", ".join(repr(e) for e in orders_products)) + ". We will call you to confirm the order. You are required to pay "+ str(checkoutt.total) + "Ksh. To confirm your order or pay via mpesa or paypal, please use the order number " + checkoutt.reference_code ,
                            ["+" + new_phone_number], )

    except Exception as e:
        print(e)
        print('NO INTERNET')
        context = {
            'results': 'error',
            'response': "No Internet "

        }

    data = CheckoutSerializer([new_checkoutorder], many=True)
    context = {
        'data': data.data
    }
    # return Response("")
    return Response(data.data, status=status.HTTP_201_CREATED)


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def getvariantoptions(request, product_id):
    variants = []
    variant_option = Product_Variant_Options.objects.filter(product = product_id)
    for order in variant_option:
        parent_variant = Variant_Option.objects.filter(id=order.variant_options.id)

        for order2 in parent_variant:
            variant = Variant.objects.filter(id=order2.variant.id).annotate(variant_option_id = Sum(order2.id, output_field = IntegerField()), variant_option_name = Value(order2.name, output_field = CharField())).first()
            variants.append(variant)
    data = CustomVariantsSerializer(variants, many=True)    
    context = {
        'data': data.data
    }

    return Response(data.data,status=status.HTTP_200_OK)

@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def getReview(request, product_id):
    review = []
    reviews = Review.objects.filter(product = product_id)
    for order in reviews:
        buyers = Buyer.objects.filter(id = order.buyer.id).annotate(ratings = Sum(order.ratings, output_field = IntegerField()), comments = Value(order.comments, output_field = CharField()), created_at = Value(order.created_at, output_field = DateTimeField())).first()
        review.append(buyers)

    data = ReviewSerializer(review, many=True)

    return Response(data.data, status=status.HTTP_200_OK)

@csrf_exempt
@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def addReview(request,product_id):
    review = []
    r_token = request.META['HTTP_AUTHORIZATION']
    new_token = r_token.split(' ', 1)[1]
    token = Token.objects.filter(key=new_token).first()
    buyer = Buyer.objects.filter(user_ptr_id=token.user.id).first()
    product = Product.objects.filter(id = product_id).first()
    comment = request.data.get("comments")
    ratings = request.data.get("ratings")

    new_review = Review.objects.create(
        buyer = buyer,
        product = product,
        comments = comment,
        ratings = int(ratings),
    )

    reviews = Review.objects.filter(product = product_id)

    for order in reviews:
        buyers = Buyer.objects.filter(id = order.buyer.id).annotate(ratings = Sum(order.ratings, output_field = IntegerField()), comments = Value(order.comments, output_field = CharField()), created_at = Value(order.created_at, output_field = DateTimeField())).first()
        review.append(buyers)

    data = ReviewSerializer(review, many=True)

    return Response(data.data, status=status.HTTP_200_OK)

@csrf_exempt
@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def getReviewStatus(request,product_id):
    review = []
    r_token = request.META['HTTP_AUTHORIZATION']
    new_token = r_token.split(' ', 1)[1]
    token = Token.objects.filter(key=new_token).first()
    buyer = Buyer.objects.filter(user_ptr_id=token.user.id).first()

    if Checkout.objects.filter(buyer = buyer, status = 'PAID').exists():
        checkout = Checkout.objects.filter(buyer = buyer, status = 'PAID')
        for order in checkout:
            products = Order_Product.objects.filter(checkout = order.id)
            for product in products:
                reviewable = Order_Product.objects.filter(product = product_id).first()
                if reviewable is not None:
                # if Order_Product.objects.filter(product = product_id).exists():
                    context = {
                            'response': 'success'
                        }
                    return Response(context, status=status.HTTP_200_OK)
                else:
                     context ={
                         'response': 'Not Found'
                     }
                     return Response(context, status=status.HTTP_400_BAD_REQUEST)   
    
    else:
        context = {
            'response': 'Not found'
        }
        return Response(context, status=status.HTTP_404_NOT_FOUND)                 

@csrf_exempt
@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def getBuyerOrders(request):
    # print(request.META['HTTP_AUTHORIZATION'])
    products = []
    r_token = request.META['HTTP_AUTHORIZATION']
    new_token = r_token.split(' ', 1)[1]
    token = Token.objects.filter(key=new_token).first()
    buyer = Buyer.objects.filter(user_ptr_id=token.user.id).first()
    if not buyer:
        return Response(
            data={
                "Message": "You are not logged in"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    wishlistProducts = Wishlist.objects.filter(buyer=buyer)
    for order in wishlistProducts:
        allwishlistproducts = Product.objects.filter(id = order.product.id).annotate(wishlist_id=Sum(order.id, output_field=IntegerField())).first()
        products.append(allwishlistproducts)
    data = CustomWishlistSerializer(products, many=True)    
    context = {
        'data': data.data
    }

    return Response(data.data,status=status.HTTP_200_OK)

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def getShortCodeSMS(request):
    phonenumber = request.data.get("phone_number")

    if Buyer.objects.filter(phone_number = phonenumber).exists():

        context = {
            'response': 'Already Registered'
        }
        return Response(context, status=status.HTTP_400_BAD_REQUEST)
    else:    
        # Initialize SDK
        # username = "Mashkys"    # use 'sandbox' for development in the test environment
        username = "eugenewere"    # use 'sandbox' for development in the test environment
        api_key = "495ade1667cabcfa21092603ff76876cd2bc01371d7e08252dc45a8c1a1b5103"      # use your sandbox app API key for development in the test environment
        # api_key = "652230d338f11fd49333722a8acba0161942b5b3efb880caf2fb21958e4fdde4"      # use your sandbox app API key for development in the test environment
        africastalking.initialize(username, api_key)
        random_code = get_random_string(length=6, allowed_chars='123456789')
        appKey = request.data.get("appSignature")
        new_phone_number = f"{254}{phonenumber[-9:]}"
        print(random_code)

        # Initialize a service e.g. SMS
        sms = africastalking.SMS


        # Use the service synchronously
        response = sms.send("<#> Your JIKONIFY code is:" + random_code + ":\n " + appKey , ["+"+new_phone_number])
        print(response)
        short_code = ShortCode.objects.create(
            phone_number = phonenumber,
            short_code = random_code,
        )
        context = {
            'response': 'success'
        }
        return Response(context, status=status.HTTP_200_OK)

        # Or use it asynchronously
        # def on_finish(error, response):
        #     if error is not None:
        #         raise error
        #     print(response)

        # sms.send("Hello Message!", ["+2547xxxxxx"], callback=on_finish)

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def getResetCodeSMS(request):
    phonenumber = request.data.get("phone_number")

    if Buyer.objects.filter(phone_number = phonenumber).exists():   
        # Initialize SDK
        username = "Mashkys"    # use 'sandbox' for development in the test environment
        api_key = "652230d338f11fd49333722a8acba0161942b5b3efb880caf2fb21958e4fdde4"      # use your sandbox app API key for development in the test environment
        africastalking.initialize(username, api_key)
        random_code = get_random_string(length=6, allowed_chars='123456789')
        appKey = request.data.get("appSignature")
        new_phone_number = f"{254}{phonenumber[-9:]}"
        print(random_code)
        # Initialize a service e.g. SMS
        sms = africastalking.SMS 


        # Use the service synchronously
        response = sms.send("<#> Your MASHKYS code is:" + random_code + ":\n " + appKey , ["+"+new_phone_number], "MASHKYS")
        print(response)

        short_code = ShortCode.objects.create(
            phone_number = phonenumber,
            short_code = random_code,
        )
        context = {
            'response': 'success'
        }
        return Response(context, status=status.HTTP_200_OK)

        # Or use it asynchronously
        # def on_finish(error, response):
        #     if error is not None:
        #         raise error
        #     print(response)

        # sms.send("Hello Message!", ["+2547xxxxxx"], callback=on_finish)
    else:
        
        context = {
            'response': 'That Number Is Not Registered'
        }
        return Response(context, status=status.HTTP_400_BAD_REQUEST)      


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def verifyCode(request):
    short_code = request.data.get("short_code","")
    phonenumber = request.data.get("phone_number","")

    codes = ShortCode.objects.filter(phone_number = phonenumber)

    if ShortCode.objects.filter(short_code = short_code).exists():
            password = request.data.get("password", "")
            new_buyer = Buyer.objects.create_user(
                # user_ptr_id=new_buyer.id,
                username = phonenumber,
                password= password,
                phone_number=phonenumber,
                is_staff=False
            )

            codes.delete()
            token, _ = Token.objects.get_or_create(user=new_buyer)
            context = {
                'token': token.key,
                'id': new_buyer.id,
                'phonenumber': new_buyer.phone_number
            }
            return Response(context,
                            status=status.HTTP_201_CREATED)
    context = {
        'response': 'Wrong Short Code'
    }
    return Response(context, status=status.HTTP_200_OK)
  

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def resetPin(request):
    short_code = request.data.get("pin")
    phonenumber = request.data.get("phone_number")

    codes = ShortCode.objects.filter(phone_number = phonenumber)
    if ShortCode.objects.filter(short_code = short_code).exists():
            user = Buyer.objects.filter(phone_number = phonenumber).first()
            token, _ = Token.objects.get_or_create(user=user)
            context = {
                'token': token.key,
                'id': user.id,
                'phonenumber': user.phone_number,
            }
            codes.delete()

            return Response(context,
                            status=HTTP_201_CREATED)
    context = {
        'response': 'Wrong Short Code'
    }
    return Response(context, status=status.HTTP_200_OK)

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def getSearchResults(request):
    result = []
    query = request.data.get("stringPojo")
    if Category.objects.filter(name__icontains = query).exists():
        categories = Category.objects.filter(name__icontains = query)
        for order in categories:
            products = Product.objects.filter(category=order.id, status = 'VERIFIED')
            result.append(products)
            # sub_category = Category.objects.filter(parent_id = order.id)
            # for sub in sub_category:
            #     sub_products = Product.objects.filter(category=sub.id, status = 'VERIFIED')
            #     result.append(products)
        data = ProductSerializer(products, many = True)

        return Response(data.data,status=status.HTTP_200_OK)

    elif Brand.objects.filter(name__icontains = query).exists():
        brands = Brand.objects.filter(name__icontains = query).first()
        products = Product.objects.filter(product_brand = brands)
        result.append(products)
        data = ProductSerializer(products, many = True)

        return Response(data.data,status=status.HTTP_200_OK)

    elif Product.objects.filter(name__icontains = query).exists():
        products = Product.objects.filter(name__icontains = query)
        result.append(products)
        data = ProductSerializer(products, many = True)

        return Response(data.data,status=status.HTTP_200_OK)

    else:
        context={
            'messsage':'No Results'
        }    

        return Response(context,status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def updateUserName(request):
    firstname = request.data.get("first_name")
    lastname = request.data.get("last_name")
    r_token = request.META['HTTP_AUTHORIZATION']
    new_token = r_token.split(' ', 1)[1]
    token = Token.objects.filter(key=new_token).first()
    buyer = Buyer.objects.filter(user_ptr_id=token.user.id).first()
    user = User.objects.filter(id=buyer.user_ptr_id).update(
        first_name = firstname,
        last_name = lastname
    )

    # user.first_name=firstname,
    # user.last_name=lastname
    # user.save()
    users = User.objects.filter(id=buyer.user_ptr_id).first()
    
    context = {
                'first_name': users.first_name,
                'last_name': users.last_name
            }

    return Response(context, status=status.HTTP_200_OK)

@csrf_exempt
@api_view(["DELETE"])
@permission_classes((IsAuthenticated,))
def cancelOrder(request, checkout_id):
    print(checkout_id)
    checkout = Checkout.objects.filter(id=checkout_id).first()
    orderProducts =  Order_Product.objects.filter(id=checkout.id)
    for orderProduct in orderProducts:
        orderProduct.delete()
    checkout.delete()
    all_checkouts=[]
    r_token = request.META['HTTP_AUTHORIZATION']
    new_token = r_token.split(' ', 1)[1]
    token = Token.objects.filter(key=new_token).first()
    buyer = Buyer.objects.filter(user_ptr_id=token.user.id).first()
    if not buyer:
        return Response(
            data={
                "Message": "You are not logged in"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    checkouts =  Checkout.objects.filter(buyer=buyer)
    for checkout in checkouts:
        all_checkouts.append(checkout)
    data = CheckoutSerializer(all_checkouts, many=True)


    context={
        'data': data.data

    }
    return Response(context, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def delivery_region(request):
    regions = Region.objects.all()
    data = RegionSerializer(regions, many=True)
    return Response(data.data,status=status.HTTP_200_OK)

@csrf_exempt
@api_view(["POST"])
def subscribertoemail(request):
    email = request.data.get("email")
    print(email)
    if not NewsLetter.objects.filter(email__exact=email):
        NewsLetter.objects.create(
            email=email
        )
        return Response(
            data={
                "message": "Successfully Subscribed"
            },
            status=status.HTTP_200_OK
        )
    else:
        return Response(
            data={
                "message": "Seems this email has been used, use another one",

            },
            status=status.HTTP_400_BAD_REQUEST
        )

@csrf_exempt
@api_view(["POST"])
# @permission_classes((AllowAny,))
def paypalpayments(request):
    print(request.data)
    # print(request.data['checkout_id'])
    print(request.data.get('checkout_id'))
    checkout_id = request.data.get("checkout_id")
    payment_id = request.data.get("payment_id")
    state = request.data.get("state")

    r_token = request.META['HTTP_AUTHORIZATION']
    new_token = r_token.split(' ', 1)[1]

    token = Token.objects.filter(key=new_token).first()
    buyer = Buyer.objects.filter(user_ptr_id=token.user.id).first()


    print(checkout_id, state,payment_id)
    chk = Checkout.objects.filter(id=int(checkout_id)).first()
    if chk:
        print(chk)
        pay_method = "PAYPAL"
        payer_reg_no = chk.reference_code
        amount = chk.total
        currency_value = 108
        if state.lower() == 'approved':
            payment_status = 'COMPLETED'
            transaction_status = 'COMPLETED'
        elif state.lower() == 'approved':
            payment_status = 'CANCELED'
            transaction_status = 'CANCELED'
        cp = CheckoutPayment.objects.create(
            checkout=chk,
            pay_method=pay_method,
            payer_reg_no=payer_reg_no,
            payer_full_name=buyer.first_name,
            payer_paying_email=buyer.email,
            business_email_paid=settings.PAYPAL_BUSINESS_EMAIL,
            country_code="KE",
            amount=amount,
            currency_amount=(chk.total)/108,
            currency_code="USD",
            currency_value=currency_value,
            pay_recipt_no=payment_id,
            transaction_recipt_no=payment_id,
            transaction_status=transaction_status,
            payment_status=payment_status,

        )
        print(cp)

        Checkout.objects.filter(reference_code=payer_reg_no).update(
            status='PAID',
        )
        print(buyer)
        return Response(
            data={
                "message": "Successfully Subscribed"
            },
            status=status.HTTP_200_OK
        )
    return Response(
        data={
            "message": "Wrong Transactipon",

        },
        status=status.HTTP_400_BAD_REQUEST
    )