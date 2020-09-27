from django.contrib.auth import get_user_model
from django.db import models
from datetime import datetime
import datetime
from datetime import timedelta
# from .models import *
from django.db.models import Sum


class County(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    number = models.IntegerField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % (self.name)


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False, blank=False)
    parent_id = models.ForeignKey('Category', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % (self.name)

    @property
    def has_children(self):
        if Category.objects.filter(parent_id=self).count() > 0:
            return True
        else:
            return False

    @property
    def children(self):
        return Category.objects.filter(parent_id=self)[:6]

    @property
    def is_child(self):
        if self.parent_id:
            return True
        else:
            return False

    def childern_count(self):
        category_childern = Category.objects.filter(parent_id=self).count()
        if category_childern:
            return category_childern
        else:
            return category_childern


class Brand(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s ' % (self.name)


class Seller(get_user_model()):
    # first_name = models.CharField(max_length=100, null=False, blank= False)
    # last_name = models.CharField(max_length=100, null=False, blank= False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    # email = models.EmailField(max_length=100, unique=True, null=False, blank=False)
    # password = models.CharField(max_length=200)
    business_no = models.CharField(max_length=100, null=False, unique=True, blank=False)
    store_logo = models.ImageField(default="no_seller_logo.jpg", upload_to='store_logo', max_length=200,
                                   null=True)  # height_field=None, width_field=None
    store_name = models.CharField(max_length=100, null=False, unique=True)

    SELLER_STATUS = (
        ('VERIFIED', 'Verified'),
        ('UNVERIFIED', 'Unverified'),
    )
    status = models.CharField(choices=SELLER_STATUS, max_length=100, default='UNVERIFIED')
    country = models.CharField(max_length=100, null=False)

    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = 'Seller'
        verbose_name_plural = 'Sellers'

    def __str__(self):
        return '%s %s (%s)' % (self.first_name, self.last_name, (self.store_name))

    @property
    def order_products(self):
        product = Product.objects.filter(seller=self)
        orderproducts = Order_Product.objects.filter(product=product)
        return orderproducts

    def ordered_products(self, product_id):
        product = Product.objects.filter(id=product_id)
        if product is None:
            return False
        order = self.order_products
        if order.filter(checkout__isnull=False):
            return True
        return False


class Product(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    unit_cost = models.FloatField(max_length=50)
    product_brand = models.ForeignKey(Brand, related_name='products', on_delete=models.CASCADE)
    short_description = models.TextField()
    long_description = models.TextField()
    featured_url = models.ImageField(default="no_product_img.jpg", upload_to="product_images",
                                     max_length=200)  # height_field=None, width_field=None
    category = models.ForeignKey(Category, related_name='categories', on_delete=models.CASCADE)
    PRODUCT_STATUS = (
        ('UNVERIFIED', 'Unverified'),
        ('Blocked', 'Blocked'),
        ('VERIFIED', 'VERIFIED'),
    )
    status = models.CharField(choices=PRODUCT_STATUS, default='UNVERIFIED', max_length=200)
    FEATURING_PRODUCT = (
        ('FEATURED', 'Featured'),
        ('NORMAL', 'Normal'),
    )
    feat_product = models.CharField(choices=FEATURING_PRODUCT, default='NORMAL', max_length=200)
    VAT_STATUS = (
        ('VAT', 'Vat'),
        ('NO_VAT', 'No_vat'),
    )
    vat_status = models.CharField(max_length=200, default='NO_VAT', choices=VAT_STATUS, blank=True, null=True)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return '%s (%s)' % (self.name, (self.seller))

    @property
    def prod_inventory(self):
        inventory = Inventory.objects.filter(product=self).first()
        if inventory:
            return inventory
        return None

    @property
    def link_inventories(self):
        inventory = Inventory.objects.filter(product=self).first()
        if inventory:
            return inventory
        else:
            return 'None'

    @property
    def unit_cost_inclusive_of_vat(self):

        if self.vat_status == 'VAT':
            cost = self.unit_cost * 1.16
            return float(cost)
        else:
            return float(self.unit_cost)

    @property
    def images(self):
        return Image.objects.filter(product=self)

    # def images(self):
    #     return Image.objects.filter(product=self)

    @property
    def product_variant_options(self):
        return Product_Variant_Options.objects.filter(product=self.id)

    @property
    def variants(self):
        variants = []
        Variant_Option.objects.filter()
        for product_variant_option in self.product_variant_options:
            variants.append(product_variant_option.variant_options.variant)
        # print(variants)
        return list(set(variants))

    @property
    def inventory_qty(self):
        inventory = Inventory.objects.filter(product=self).first()
        if inventory is not None:
            inventoryqty = inventory.quantity
            if inventoryqty > 0:
                return int(inventoryqty)
            else:
                return 'Not In Stock'
        else:
            return 0

    @property
    def price_after_offer(self):
        product = Product.objects.filter(id=self.id).first()
        offer = Offer.objects.filter(product=product).first()
        if offer is not None:

            discount_price = offer.discount
            # offer_cost = (100 - float(discount)) / 100 * float(product.unit_cost_inclusive_of_vat)
            # # print(offer_cost)
            return float(discount_price)
        else:
            return product.unit_cost


class Buyer(get_user_model()):
    # first_name = models.CharField(max_length=100, null=False, blank=False)
    # last_name = models.CharField(max_length=100, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False, unique=True)

    # email = models.EmailField(max_length=100, unique=True, null=False)
    # password = models.CharField(max_length=200)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

    class Meta:
        verbose_name = 'Buyer'
        verbose_name_plural = 'Buyers'

    # def cart_variant(self):
    #     variants=[]
    #     # order_variant_options = OrderProductVariantOption.objects.filter(orderProduct__product=self)
    #     variant = Variant.objects.filter(variant_options__orderproductvariantoption__orderProduct_id=self,)
    #     buyer_orders = Order_Product.objects.filter(buyer=self, checkout_id__isnull=True, checkout__status='PENDING')
    #     for order in buyer_orders:
    #         variants.append(order)

    @property
    def buyer_order_count(self):
        order_count = Order_Product.objects.filter(buyer=self.id)
        if order_count:
            return order_count.count
        return 0

    @property
    def byer_orders(self):
        order = Order_Product.objects.filter(buyer=self, checkout_id__isnull=False, checkout__status='PENDING')
        if order is not None:
            return self
        return False

    def buyer_with_orders(self):
        order = Order_Product.objects.filter(buyer=self, checkout_id__isnull=False, checkout__status='PENDING')

    @property
    def cart_total(self):
        total = 0
        for order_product in Order_Product.objects.filter(buyer=self, product__wishlist__isnull=True,
                                                          checkout_id__isnull=True):
            total += float(order_product.total)
        return total

    @property
    def wishlist(self):
        wishlists = Wishlist.objects.filter(buyer=self)
        return wishlists

    @property
    def order_products(self):
        orderproducts = Order_Product.objects.filter(buyer=self, product__wishlist__isnull=True)
        return orderproducts

    def product_in_wishlist(self, product_id):
        product = Product.objects.filter(id=product_id).first()
        if product is None:
            return False
        wishlists = self.wishlist
        if wishlists.filter(product=product).count() > 0:
            return True
        return False

    @property
    def cart_total_plus_vat(self):
        return self.cart_total * 1.16

    def products_with_vat(self, product_id):
        prod = Product.objects.filter(vat_status='VAT', id=product_id)
        return prod

    @property
    def vat_cost(self):
        total = 0

        orderproducts = Order_Product.objects.filter(buyer=self, product__wishlist__isnull=True,
                                                     product__vat_status='VAT')
        for order_product in orderproducts:
            total += float(order_product.total)
        # print(total)
        vat = 0.16 * total
        # print(vat)
        return vat

    def product_wishlist_delete(self, product_id):
        product = Product.objects.filter(id=product_id).first()
        if product is not None:
            return True
        else:
            return False

    def product_in_cart(self, product_id):
        product = Product.objects.filter(id=product_id).first()
        if product is None:
            return False
        cart = self.order_products
        if cart.filter(product=product, checkout__isnull=True).count() > 0:
            return True
        return False


class Image(models.Model):
    product = models.ForeignKey(Product, related_name="products", on_delete=models.CASCADE)
    image = models.FileField(default="no_products_image.jpg", upload_to='images')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s (%s)' % (self.image, (self.product.name))


class Review(models.Model):
    buyer = models.ForeignKey(Buyer, related_name='buyers', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    comments = models.TextField(max_length=100)
    ratings = models.IntegerField(default=1, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s (%s)' % (self.comments, (self.ratings))

    @property
    def single_product_review(self):
        product = Product.objects.filter(id=self.product)
        return product


class Wishlist(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s (%s)' % (self.buyer.first_name, (self.product.name))


class Region(models.Model):
    name = models.CharField(max_length=50, null=False)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, blank=False, null=False)
    region_cost = models.FloatField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s (%s)' % (self.name, (self.region_cost))


# we have no string being returned foe wishlist
class Checkout(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    phonenumber = models.CharField(max_length=20, null=False)
    total = models.FloatField(default=0, )
    reference_code = models.CharField(max_length=10, null=False)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True , blank=True)
    address = models.CharField(max_length=200, null=True , blank=True)
    amount_paid = models.FloatField(default=0, )
    shipping_cost = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    CHECKOUT_STATUS = (
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
    )
    status = models.CharField(choices=CHECKOUT_STATUS, max_length=100, default='PENDING')
    PAYMENTSTATUS=(
        ('CASH','Cash'),
        ('MPESA', 'Mpesa'),
        ('PAYPAL', 'Paypal'),
    )
    paymentchoice = models.CharField(choices=PAYMENTSTATUS, default="CASH", max_length=200, null=False, blank=False)
    class Meta:
        verbose_name = 'Checkout'
        verbose_name_plural = 'Checkouts'

    def __str__(self):
        return '%s ' % (self.buyer.first_name)

    def ord_qnty(self, order_id):
        order = Order_Product.objects.filter(id=order_id).first()

        return order.quantity

    @property
    def buyer_with_this_checkout(self):
        ref_code = self.reference_code
        order = Order_Product.objects.filter(checkout__reference_code__exact=ref_code).first()
        return order

    @property
    def buyer_order_with_reference_code(self):
        ref_code = self.reference_code
        orders = Order_Product.objects.filter(checkout__isnull=False, checkout__reference_code__exact=ref_code,
                                              checkout__status__iexact='PENDING')
        buyers = []
        groups = []
        for order in orders:
            buyers.append(order.buyer)
        for buyer in buyers:
            groups.append(buyer)

        return list(set(groups))


class CheckoutPayment(models.Model):
    pay_method = models.CharField(max_length=200, null=False, blank=False)
    checkout = models.ForeignKey(Checkout, on_delete=models.SET_NULL, null=True, blank=True)
    payer_reg_no = models.CharField(max_length=200, null=True, blank=True)
    payer_full_name = models.CharField(max_length=200, null=True, blank=True)
    payer_paying_email = models.CharField(max_length=200, null=True, blank=True)
    business_email_paid = models.CharField(max_length=200, null=True, blank=True)

    country_code = models.CharField(max_length=200, null=True, blank=True)
    amount = models.CharField(max_length=200, null=False, blank=False)

    currency_amount = models.CharField(max_length=200, null=True, blank=True)
    currency_code = models.CharField(max_length=200, null=True, blank=True)
    currency_value = models.CharField(max_length=200, null=True, blank=True)

    pay_recipt_no = models.CharField(max_length=200, null=False, blank=False)
    transaction_recipt_no = models.CharField(max_length=200, null=False, blank=False)
    CUSTOMER_PAYMENT_STATUS = {
        ('UNPAID', 'Unpaid'),
        ('CANCELED', 'Canceled'),
        ('COMPLETED', 'Completed'),
        ('PARTIAL', 'Partial'),
    }
    payment_status = models.CharField(max_length=200, choices=CUSTOMER_PAYMENT_STATUS, default='UNPAYED', null=True,
                                      blank=True)
    transaction_status = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % (self.payer_reg_no)



class Order_Product(models.Model):
    product = models.ForeignKey(Product, related_name='orders', on_delete=models.CASCADE)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    checkout = models.ForeignKey(Checkout, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=1)
    total = models.FloatField(max_length=100, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s %s(%s)' % (self.buyer.first_name, self.product.name, (self.quantity))

    @property
    def qnty(self):

        return int(self.quantity)






        # buyers=[]
        # buyer_orders = Order_Product.objects.filter(checkout__reference_code=self.checkout.reference_code)
        #
        # for buyer_order in buyer_orders:
        #     buyers.append(buyer_order)
        # print(buyers)
        # return list(set(buyers))

    @property
    def orderpaymentttt(self):
        order_payment = Order_payment.objects.filter(checkout=self.checkout).first()
        if order_payment is not None:
            return order_payment
        return None

    @property
    def buyer_orders(self):
        if self.buyer:
            return True
        return False

    @property
    def order_of_a_buyer(self):
        order = Order_Product.objects.filter(buyer_id=self.buyer.id, checkout__isnull=False, checkout__status='PENDING')
        if order is not None:
            return self.buyer
        return False

    @property
    def ordertotal(self):
        totall = self.total
        return totall

    @property
    def order_variants(self):
        variants = []
        variant_options = OrderProductVariantOption.objects.filter(orderProduct=self)
        for option in variant_options:
            variants.append(option.variantOptions)

        return list(set(variants))

    @property
    def order_variants_for_excel(self):
        variants = []
        # product = Product.objects.filter(id=self.product.id).first()
        variant_options = OrderProductVariantOption.objects.filter(orderProduct=self)
        for option in variant_options:
            variants.append(option.variantOptions)
        if len(variants) >= 0:
           return (i for i in variants)
        else:
            return 'NONE'



class Order_payment(models.Model):
    checkout = models.ForeignKey(Checkout, on_delete=models.CASCADE)
    amount = models.FloatField()
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, null=True, blank=True)
    balance = models.FloatField(default=0)
    payment_refrence = models.CharField(max_length=200, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s %s' % (self.checkout.buyer.phone_number, self.amount)

    def payment_buyer(self):
        buyers = []
        ordrs = Order_Product.objects.filter(checkout_id=self.checkout)
        for order in ordrs:
            buyers.append(order.order_of_a_buyer)


# #check on status
class Payment(models.Model):
    checkout = models.ForeignKey(Checkout, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50)
    amount = models.FloatField()
    reference_code = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    PAYMENT = (
        ('VERIFIED', 'verified'),
        ('UNVERIFIED', 'unverified'),
    )
    status = models.CharField(choices=PAYMENT, max_length=100, default='UNVERIFIED')


class Order_Delivery(models.Model):
    checkout = models.ForeignKey(Checkout, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    DELIVERY_STATUS = (
        ('DELIVERED', 'Deliverd'),
        ('UNDELIVERED', 'Undelivered'),
    )
    delivery_status = models.CharField(max_length=50, choices=DELIVERY_STATUS, default='UNDELIVERED')
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % (self.delivery_status)


# can this offer return an product image alongside the offer
class Offer(models.Model):  #
    offer = models.CharField(max_length=50)
    product = models.ForeignKey(Product, related_name='offers', on_delete=models.CASCADE)
    discount = models.FloatField(null=False, default=0)
    start_time = models.DateTimeField(default=datetime.datetime.now())
    end_time = models.DateTimeField(default=datetime.datetime.now())
    # duration=models.DateTimeField(default=datetime.datetime.now())     #  auto_now_add=True
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s (%s)' % (self.product.name, (self.offer))

    @property
    def offer_percentage(self):

        offer = self.product
        if offer is not None:
            current_price = offer.unit_cost_inclusive_of_vat
            offer_price = self.discount

            percent = ((current_price - offer_price) / (current_price + offer_price)) * 100

            return int(percent)
        else:
            return None


class Carousel(models.Model):
    image = models.ImageField(default="no_carousel.jpg", upload_to='couresel')  # height_field=None, width_field=None,
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    description = models.CharField(max_length=150, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s %s ' % (self.image, self.description)


class Inventory(models.Model):
    product = models.ForeignKey(Product, related_name='product', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s %s' % (self.product.name, (self.quantity))


class Variant(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % (self.name)

    @property
    def variant_options(self):
        return Variant_Option.objects.filter(variant_id=self.id)

    # def options(self):
    #     variant_options=[]
    #     Product = Product_Variant_Options.objects.filter(varia)
    #     options = Variant_Option.objects.filter(variant=self)
    #     for option in options:
    #        variant_options.append(option)
    #
    #     return list(set(variant_options))

    def product_variant_options(self):
        options = Product_Variant_Options.objects.filter(variant_options__variant=self.id)
        print(options)
        return options


class Variant_Option(models.Model):
    variant = models.ForeignKey(Variant, related_name='variant_options', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s (%s)' % (self.variant.name, (self.name))


class OrderProductVariantOption(models.Model):
    orderProduct = models.ForeignKey(Order_Product, on_delete=models.CASCADE)
    variantOptions = models.ForeignKey(Variant_Option, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s %s' % (self.orderProduct.product.name, self.variantOptions.name)

    @property
    def cart_variant_option(self):
        variantoptions = Variant_Option.objects.filter(variant=self.variantOptions.id)

        return variantoptions

    @property
    def order_variant(self):
        variants = []
        orders = self.variantOptions.variant.name
        for order in orders:
            variants.append(order)
        return list(set(variants))


class Product_Variant_Options(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant_options = models.ForeignKey(Variant_Option, on_delete=models.CASCADE, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s (%s)' % (self.product.name, (self.variant_options))

    def variant(self):
        return self.variant_options.variant


class OrderPayment(models.Model):
    order_product = models.ForeignKey(Order_Product, on_delete=models.CASCADE)
    # checkout = models.ForeignKey(Checkout, on_delete=models.CASCADE)
    amount = models.IntegerField(blank=False, null=False)
    payment_reference = models.CharField(max_length=100, null=False, blank=False)
    date = models.DateTimeField(default=datetime.datetime.now())
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s (%s)' % (self.order_product.product.name, (self.amount))


class Order(models.Model):
    shipping_cost = models.IntegerField(blank=False, null=False)
    order_total = models.IntegerField(blank=False, null=False)
    balance = models.IntegerField(blank=False, null=False)
    PAYMENT_STATUS = (
        ('PAID', 'Paid'),
        ('UNPAID', 'Unpaid'),
    )
    payment_status = models.CharField(choices=PAYMENT_STATUS, default='UNPAID', max_length=200, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s (%s)' % (self.order_total, (self.payment_status))

class NewsLetter(models.Model):
    email = models.CharField(max_length=100, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % (self.email)

class BroadcastNewsLetter(models.Model):
    newsletter = models.ForeignKey(NewsLetter, on_delete=models.CASCADE)
    msg= models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % (self.msg)

