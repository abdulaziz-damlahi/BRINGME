from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('addtoshopcart/<int:id>', views.addtoshopcart, name='addtoshopcart'),
    path('deletefromcart/<int:id>', views.deletefromcart, name='deletefromcart'),
    path('orderproduct', views.orderproduct, name='orderproduct'),
    path('orders/', views.order_user, name='order_user'),
    path('orderdetail/<int:id>', views.user_orderdetail, name='user_orderdetail'),


]