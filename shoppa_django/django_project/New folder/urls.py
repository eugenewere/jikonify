from django.urls import path
from django.conf.urls import include, url
from androidAuthApi import views
from rest_framework.authtoken import views as authviews


urlpatterns = [
    path('users/', views.UserList.as_view()),
    path('user/details/<int:pk>/', views.UserDetail.as_view()),
    path('api-token-auth/', authviews.obtain_auth_token),
    path('signup/',views.signup2),
    path('login/',views.login),
    path('orders/',views.OrderList.as_view()),
    path('orders/details/<int:pk>/', views.OrderDetail.as_view()),
    path('category/',views.CategoryList.as_view()),
    path('product/',views.ProductList.as_view()),
    path('product/details/<int:fk>/',views.ProductDetails.as_view())
]

