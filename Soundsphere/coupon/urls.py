from django.urls import path
from . import views

urlpatterns = [
    path('',views.coupon,name='coupon'),
    path('user_coupon/',views.user_coupon,name='user_coupon'),
    path('add_coupon',views.add_coupon,name='add_coupon'),
    path('edit_coupon/<int:id>/',views.edit_coupon,name='edit_coupon'),
    path('delete_coupon/<int:id>',views.delet_coupon,name='delete_coupon')
]