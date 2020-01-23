from rest_framework import serializers
from shoppy.models import Buyer, Order_Product, Checkout, Category, Product

class buyersSerializer(serializers.ModelSerializer):

    class Meta:
        model =  Buyer
        fields = ('id', 'username','first_name','last_name','email','phone_number',)

class OrdersSerializer(serializers.ModelSerializer):
    buyers = buyersSerializer(many=True, read_only=True)

    class Meta:
        model = Order_Product
        fields = ('id','product','buyers','checkout','quantity','total','created_at',)

class CheckoutSerializer(serializers.ModelSerializer):
    orders = OrdersSerializer(many=True, read_only=True)

    class Meta:
        model = Checkout
        fields = ('reference_code','orders','created_at',)

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name',)

class ProductsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id','name','short_description','product_brand','unit_cost','featured_url',)