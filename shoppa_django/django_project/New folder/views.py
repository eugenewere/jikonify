from shoppy.models import Buyer, Order_Product, Category, Product
from .serializers import buyersSerializer, OrdersSerializer, CheckoutSerializer, CategorySerializer, ProductsSerializer
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
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK
from rest_framework.views import APIView
# from django.http import HttpResponse
# from django.shortcuts import get_object_or_404


class UserList(generics.ListAPIView):
    queryset = Buyer.objects.all()
    serializer_class = buyersSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Buyer.objects.all()
    serializer_class = buyersSerializer

class OrderList(generics.ListAPIView):
    queryset = Order_Product.objects.all()
    serializer_class = OrdersSerializer

class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order_Product.objects.all()
    serializer_class = OrdersSerializer

class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductsSerializer

class ProductDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductsSerializer


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
    username = request.data.get("username")
    password = request.data.get("password")
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
                
# class ChangePassword(generics.UpdateAPIView):
#     serializer_class = UserPasswordChangeSerializer
#     model = Buyer
#     permission_classes = (IsAuthenticated,)

#     def get_object(self, queryset=None):
#         return self.request.user