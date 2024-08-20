from django.urls import path
from . import views

urlpatterns = [
    path('',views.offer,name='offer'),
    path('product_offer/',views.product_offer,name='product_offer'),
    path('brand_offer/',views.brand_offer,name='brand_offer'),
    path('choose_brand/',views.choose_brand,name='choose_brand'),
    path('add_brand_offer/<int:id>',views.add_brand_offer,name='add_brand_offer'),
    path('edit_brand_offer/<int:id>',views.edit_brand_offer,name='edit_brand_offer'),\
    path('delete_brand_offer/<int:id>',views.delete_brand_offer,name='delete_brand_offer'),
    path('choose_product/',views.choose_product,name='choose_product'),
    path('add_product_offer/<int:id>',views.add_product_offer,name='add_product_offer'),
    path('edit_product_offer/<int:id>',views.edit_product_offer,name='edit_product_offer'),\
    path('delete_product_offer/<int:id>',views.delete_product_offer,name='delete_product_offer'),
]   