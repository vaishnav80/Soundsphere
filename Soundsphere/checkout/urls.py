from django.urls import path
from . import views
urlpatterns = [
    path('',views.checkout,name='checkout'),
    path('conform/',views.conform,name='conform'),
    path('chooseaddress/',views.select_address,name='selectaddress'),
    path('success/',views.successpage,name='successpage'),
    path('shoping_address/',views.shop_address,name='shop_address'),
    path('create_order/', views.create_order, name='create_order'),
    path('use_coupon',views.use_coupon,name='use_coupon'),
    path('remove_coupon/',views.remove_coupon,name='remove_coupon'),
    path('save_subtotal/', views.save_subtotal, name='save_subtotal'),
] 