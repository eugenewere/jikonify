from rest_framework import serializers

from shoppy.models import Buyer, Category, Product, Order_Product, Brand, Variant, Carousel, Offer
from shoppy.models import Wishlist, Region, Checkout, Product_Variant_Options, Variant_Option, Review, Image
from shoppy.models import Inventory, OrderProductVariantOption

class buyersSerializer(serializers.ModelSerializer):

    class Meta:
        model =  Buyer
        fields = ('id', 'username')

class wishlistSerializer(serializers.ModelSerializer):

    class Meta:
        model =  Wishlist
        fields = '__all__'

class OrderProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order_Product
        fields = ('id','buyer','product','checkout','quantity','total','created_at',)

class OfferSerializer(serializers.ModelSerializer):

    class Meta:
        model = Offer
        fields = ('offer', 'discount')

class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ('image',)

class InventorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Inventory
        fields = ('quantity',)                    

class ProductSerializer(serializers.ModelSerializer):
    offers = OfferSerializer(many=True)
    products = ImageSerializer(many=True)
    product = InventorySerializer(many= True)

    class Meta:
        #changed
        model = Product

        fields = ('id','name','unit_cost','product_brand','short_description','long_description','featured_url','vat_status','offers','category','products','product')



class BrandSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=False)

    class Meta:
        model = Brand
        fields = ('id','name','products')

class AndroidProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id','name','unit_cost','product_brand','short_description','featured_url','category')

class AllProductsSerializer(serializers.ModelSerializer):
    categories = serializers.StringRelatedField(many=True)

    class Meta:
        model = Category
        fields = ('name','categories',)

class CategorySerializer(serializers.ModelSerializer):
    # brands = BrandSerializer(many=True, read_only=False)

    class Meta:
        model = Category
        fields = ('id','name',)

class RegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Region
        fields = ('id','name','region_cost')

class CustomCartSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    unit_cost = serializers.FloatField()
    product_brand = serializers.CharField()
    short_description = serializers.CharField()
    featured_url = serializers.CharField()
    vat_status = serializers.CharField()
    order_id = serializers.IntegerField()
    quantity = serializers.FloatField()
    total = serializers.FloatField()

class CustomWishlistSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    unit_cost = serializers.FloatField()
    product_brand = serializers.CharField()
    short_description = serializers.CharField()
    featured_url = serializers.CharField()
    wishlist_id = serializers.IntegerField()

class CustomVariantsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    variant_option_id = serializers.IntegerField()
    variant_option_name = serializers.CharField()  

class CheckoutSerializer(serializers.ModelSerializer):

    class Meta:
        model = Checkout
        fields = '__all__'

class ParentVariantSerializer(serializers.ModelSerializer):
    # variant_options = serializers.StringRelatedField(many=True)

    class Meta:
        model = Variant
        fields = ('id','name',)

class VariantsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Variant_Option
        fields = ('id','name','variant')       

class VariantOptionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product_Variant_Options
        fields = ('id','product','variant_options',)

class CarouselSerializer(serializers.ModelSerializer):

    class Meta:
        model = Carousel
        fields = '__all__'

class ReviewSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    buyer = serializers.CharField()
    ratings = serializers.IntegerField()
    comments = serializers.CharField()
    created_at = serializers.DateTimeField()

class CartVariantSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderProductVariantOption
        fields = '__all__'    