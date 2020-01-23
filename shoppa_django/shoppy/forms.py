
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import *
from django import forms


class BuyerSignUpForm(UserCreationForm):

    class Meta:
        model = Buyer
        fields = ['password1','password2','username',]












# seller
class SellerSignUpForm(UserCreationForm):

     class Meta:
         model = Seller
         fields = ('email','phone_number','business_no','store_logo','store_name','country','first_name','last_name','username',)

     def clean_username(self):
         super(SellerSignUpForm, self).clean()
         username = self.cleaned_data.get('username')
         if User.objects.filter(username__iexact=username).exists():
             raise forms.ValidationError('Username already exists')
         return username

     def clean_email(self):
         super(SellerSignUpForm, self).clean()
         email = self.cleaned_data.get('email')
         if User.objects.filter(email__iexact=email).exists():
             raise forms.ValidationError('A user has already registered using this email')
         return email

     def clean_password2(self):
         super(SellerSignUpForm, self).clean()
         password1 = self.cleaned_data.get('password1')
         password2 = self.cleaned_data.get('password2')
         if password1 and password2 and password1 != password2:
             raise forms.ValidationError('Passwords must match')
         return password2

     def clean_phone_number(self):
         super(SellerSignUpForm, self).clean()
         phone_number = self.cleaned_data.get('phone_number')
         if Seller.objects.filter(phone_number__iexact=phone_number) and Buyer.objects.filter(phone_number__iexact=phone_number):
             raise forms.ValidationError('Phone number is used by someone else')
         return phone_number

    #seller update form


class SellerUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','username',)


class SellerForm(forms.ModelForm):
        class Meta:
            model = Seller
            fields = ('phone_number','business_no','store_logo','store_name','country',)









class ProductForm(forms.ModelForm):

    class Meta:
        model =Product
        fields= ['vat_status', 'name', 'unit_cost', 'product_brand', 'short_description', 'long_description','featured_url','seller','category',]




class ImagesForm(forms.ModelForm):

    class Meta:
        model= Image
        fields=['image', 'product',]




class ProductVariantOptionForm(forms.ModelForm):

    class Meta:
        model= Product_Variant_Options
        fields =['product','variant_options',]



class InventoryForm(forms.ModelForm):

    class Meta:
        model = Inventory
        fields = ['product', 'quantity',]
class AddBrandForm(forms.ModelForm):

    class Meta:
        model =Brand
        fields =['name',]

class CarouselImageForm(forms.ModelForm):

    class Meta:
        model = Carousel
        fields = ['image','description','product','seller']

class RegionsForm(forms.ModelForm):

    class Meta:
        model = Region
        fields = ['name','region_cost','seller']

class VariantForm(forms.ModelForm):

    class Meta:
        model = Variant
        fields = ['seller','name',]

class VariantOptionForm(forms.ModelForm):

    class Meta:
        model = Variant_Option
        fields = ['name','variant','seller',]

class AddToWishList(forms.ModelForm):

    class Meta:
        model = Wishlist
        fields = ['buyer','product']

class OrderProductForm(forms.ModelForm):
     class Meta:
         model = Order_Product
         fields = ['quantity', 'product','buyer','total']

class OrderProductVariantOptionForm(forms.ModelForm):
     class Meta:
         model = OrderProductVariantOption
         fields =['orderProduct','variantOptions']

class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['name','parent_id']


class OfferForm(forms.ModelForm):

    class Meta:
        model= Offer
        fields = ['offer', 'product', 'discount', 'start_time', 'end_time',]

class ChangePasswordForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['password']