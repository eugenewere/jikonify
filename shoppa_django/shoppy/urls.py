from django.conf.urls import url
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView, \
   PasswordResetDoneView
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views


app_name = 'Shoppy'
urlpatterns =[
   # path('', views.setcookie),
   path('', views.home, name='shoppy-home'),
   path('cart/', views.cart, name='shoppy-cart'),
   path('register/', views.buyer_register, name='shoppy-buyer-reg'),
   path('seller_register/', views.seller_register, name='shoppy-seller-reg'),
   path('login/', views.user_login, name='shoppy-login'),
   path('logout/', views.logout_view, name='shoppy-logout'),
   path('products_list/', views.productsList, name='product_list'),
   path('user_account/' , views.user_account, name='shoppy-user_account' ),
   path('checkout/' , views.checkout, name='shoppy-view_checkout' ),
   path('search/' , views.search, name="searchbar"),
   path('wishlist/' , views.wishlist, name="wishlist"),

   path('howtopay/', views.how_to_pay, name='how_to_pay'),

   path('product_filter/', views.product_filter, name='product_filter'),




   #wishlist
   path('add_to_wishlist/<int:product_id>/<str:source>' , views.addToWishlist, name='add_to_wishlist' ),
   path('remove_from_wishlist/<int:wishlist_id>/<str:source>' , views.unWishProduct, name='remove_from_wishlist' ), #delete wishlist/unwished
   path('remove_from_wishlist/all/' , views.unWish_All_Products, name='remove_all_from_wishlist' ), #delete all wishlist/unwished

   #view product details
   path('details/<int:product_id>/', views.productDetails, name='shoppy_product_details'),
         # reviews
         # path('make_reviews/', views.productReview, name='shoppy_product_review'),

   #cart
   path('cart/', views.cart, name='shoppy-cart'),
   path('addto/cart/<int:product_id>/', views.addCart, name='shoppy-add-cart'),
   path('deletefrom/cart/<int:order_id>/', views.deleteCartProduct, name='shoppy_delete_cart_product'),

   # checkout
   path('confirmcheckout/', views.confirmCheckout, name='shoppy-checkout'),

   # useraccount password change
   path('user_account/change_password', views.change_password, name='change_password'),

   # password reset

   path('pin_reset/', views.password_resett, name='password_resett'),
   path('getpinShortcode/', views.getShortcode, name='getpinShortcode'),
   path('verifyCode/', views.verifyCode, name='verifyCode'),
   path('verifypassword/', views.verifypassword, name='verifypassword'),
   path('pin_confirm/', views.pin_confirmm, name='password_confirmm'),
   path('new_pin/', views.new_pin, name='new_pin'),



   # path('password_reset/', auth_views.PasswordResetView.as_view(
   #    template_name='shoppy/registration/password_reset.html',
   #    email_template_name='shoppy/registration/password_reset_email.html',
   #    subject_template_name='shoppy/registration/password_reset_subject.txt',
   #    success_url=reverse_lazy('Shoppy:password_reset_done')
   # ), name='password_reset'),
   #
   # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
   #    template_name='shoppy/registration/password_reset_done.html',
   # ), name='password_reset_done'),
   #
   # path('password_reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
   #    template_name='shoppy/registration/password_reset_confirm.html',
   #    success_url=reverse_lazy('Shoppy:password_reset_complete')
   # ), name='password_reset_confirm'),
   #
   # path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(
   #    template_name='shoppy/registration/password_reset_complete.html',
   # ), name='password_reset_complete'),

   path('deleteme/', views.deleteme, name= 'deleteme'),

   path('all_buyers_orders/', views.all_buyers_orders, name= 'all_buyers_orders'),
   path('all_buyers_order_products/<str:reference_code>', views.all_buyers_order_products, name= 'all_buyers_order_products'),
   path('orders_payment_opions/<int:checkout_id>', views.orders_payment_opions, name= 'orders_payment_opions'),



   path('assNewsLetter/<str:source>', views.assNewsLetter, name= 'assNewsLetter'),


]





