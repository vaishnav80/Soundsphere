from django.urls import *
from . import views

urlpatterns = [
    path('',views.profile,name='profile'),
    path('address/',views.address,name='address'),
    path('orders/',views.orders,name='orders'),
    path('image/',views.add_photo,name='addphoto'),
    path('addaddress/',views.addaddress,name='addadd'),
    path('deleteaddress/<int:id>',views.deleteaddress,name='deleteaddress'),
    path('editaddress/<int:num>/<int:id>',views.editaddress,name='editaddress'),
    path('ordered_product/<int:id>',views.ordered_product,name='ordered_product'),
    path('change-status/<int:id>/<str:status>/<str:product>/', views.change_status, name='change_status'),
   
]