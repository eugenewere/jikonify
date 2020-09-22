from django.urls import path
from .views import GeneratePDF, ListUsers, GenerateProductPDF,  ListOrdersadmin

from . import views

app_name = 'ShoppyAdmin'
urlpatterns = (

   path('', views.home, name='shoppy-admin-home'),
   path('sellers/', views.sellers, name='shoppy-admin-sellers'),
   path('orders/', views.orders, name='shoppy-admin-orders'),
   path('login/', views.user_login, name='shoppy-admin-login'),
   path('all/productsreviews/', views.reviews, name='shoppy-admin-reviews'),
   path('singleproduct/review/<int:product_id>/', views.single_product_review, name='single_product_review'),
   path('buyers/', views.buyers, name='shoppy-admin-buyers'),
   path('useraccount/', views.userAccount, name='shoppy-user-account'),
   path('adminaccount/', views.adminAccount, name='shoppy-admin-account'),
   path('useraccount/changepassword/', views.changepassword, name='shoppy-changepassword'),
   path('payments/', views.payments, name='shoppy-payments'),
   path('editpayments/<int:Order_payment_id>', views.edit_payments, name='shoppy_updated_payments'),
   path('buyerOrders/<str:reference_code>', views.buyerOrders, name='shoppy-buyer_orders'),
   path('buyerOrdersCancel/<str:reference_code>', views.buyerOrdersCancel, name='shoppy-buyer_orders_cancel'),
     # extras
      path('pdf/orders/', GeneratePDF.as_view(), name='orders_generated_pdf'),
      path('xcel/orders/', views.export_users_xls, name='export_users_xl'),
      path('xcel/orders/date', views.export_users_xls_date, name='export_users_xl_date'),
      path('productspdf/', GenerateProductPDF.as_view(), name='products_generated_pdf'),
      path('users/chart/', ListUsers.as_view(), name='users_chart'),
      path('orders/chart/', views.ListOrders, name='orders_chart'),
      path('orders/chart/admin', ListOrdersadmin.as_view(), name='orders_chartadmin'),
     # extras
   # seller
   path('seller_status/<int:seller_id>', views.sellerStatusChange, name='shoppy-admin-status-change'),

   #products
   path('view/products/', views.view_all_products, name="shoppy_admin_view_all_products"),
   path('view/all/products/', views.view_products, name="view_products"),
   # path('filter_products/', views.fillter_products_per_seller, name="fillter_products_per_seller"),

   path('edit/product/<int:product_id>', views.edit_product, name="shoppy_admin_edit_product"),
   path('delete/product/<int:product_id>', views.product_delete, name='product_delete'),

   #featuredProducts
   path('products/featured/products', views.featured_products, name='featuredproduct'),
   path('featured/product/change/status/featured/<int:product_id>', views.featured_products_featured, name='featured_products'),
   path('featured/product/change/status/normal/<int:product_id>', views.normal_products_normal, name='nomal_products'),

   path('products/verified/<int:product_id>/', views.verify_product, name='verify_product'),
   path('products/unverified/<int:product_id>/', views.unverify_product, name='unverify_product'),

   #category
   path('view_category/', views.view_category, name='shoppy_admin_add_category'),
   path('addingcategory/', views.addingcategory, name='shoppy_adding_category'),
   path('deletecategory/<int:category_id>', views.deletecategory, name='shoppy_delete_category'),
   path('editcategory/<int:category_id>', views.editcategory, name='shoppy_edit_category'),
   path('view_sub_category/<int:category_id>', views.view_sub_category, name='shoppy_view_sub_category'),


   # brand
   path('add_brand/', views.add_brand, name='shoppy_admin_add_brand'),
   path('delete/brand/<int:brand_id>', views.brand_delete, name='delete_brand'),
   path('edit/brand/<int:brand_id>', views.brand_edit, name='brand_edit'),

   #image
   path('delete/image/<int:image_id>', views.image_delete, name='delete_product_image'),

   #regions
   path('viewregions/', views.view_regions, name='shoppy-admin-view-regions'),
   path('regions/edit/<int:region_id>', views.edit_regions, name='shoppy-admin-edit-regions'),
   path('regions/delete/<int:region_id>', views.delete_regions, name='shoppy-admin-delete-regions'),

   #carousell
   path('view/carousel/', views.view_carousel, name='view_carousel'),
   path('carousel/delete/<int:carousel_id>', views.carousel_delete, name='carousel-delete'),
   path('carousel/edit/<int:carousel_id>', views.carousel_edit, name='carousel-edit'),

   #variants
   path('variants/', views.variants, name='variants'),
   path('variants/delete/<int:variant_id>', views.variant_delete, name='variant_delete'),
   path('variants/edit/<int:variant_id>', views.variant_edit, name='variant_edit'),

   #variant options
   path('variantsOptions/add/', views.variants_options, name='variants-options'),
   path('variantsOptions/delete/<int:variant_option_id>', views.variants_options_delete, name='variants-options-delete'),
   path('variantsOptions/edit/<int:variant_option_id>', views.variants_options_edit, name='variants-options-edit'),

   # offer
   path('offers/', views.offer, name='view_product_offer'),
   path('addOffer/',views.addOffer, name="adding_offers"),
   path('editOffer/<int:offer_id>',views.editOffer, name="edit_offers"),
   path('deleteOffer/<int:offer_id>',views.deleteOffer, name="delete_offer"),

   # reports
   path('allreports/', views.viewAllReports, name='view_all_reports'),

   #inventory
   path('updateInventory/<int:product_id>', views.update_Inventory, name='updateInventory'),


   #newsletter
   path('viewnewsletter/', views.viewnewsletter, name='viewnewsletter'),
   path('replynewsletter/', views.replynewsletter, name='replynewsletter'),
   path('replymassnewsletter/', views.replymassnewsletter, name='replymassnewsletter'),

)





