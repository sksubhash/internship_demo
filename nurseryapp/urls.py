from django.urls import path
from nurseryapp import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.user_login, name='login'),
    path('registration', views.user_registration, name='registration'),
    path('logout', views.user_logout, name='logout'),
    path('home', views.nursery_home, name='Nursery Home'),
    path('addplants', views.addplants, name='Add Plants'),
    path('nursery', views.nursery, name='Nursery'),
    path('shop', views.shop, name='Shop'),
    path('shop_details', views.shop_details, name='Shop Details'),
    path('checkout', views.checkout, name='Checkout'),
    path('nurseries@', views.nurseries_registration, name='Nurseries Registration'),
    path('order_accept', views.order_accept, name='Order Accept'),
    path('order_done', views.order_done, name='Order Done'),
]
