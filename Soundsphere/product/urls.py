from django.urls import path

from . import views

urlpatterns = [
    path('',views.product_list,name='product_list'),
    path('product_status/<int:id>',views.product_status,name='product_status'),
    path('product/add/',views.add,name='add'),
    path('product/add_images/<int:id>',views.add_images,name='add_images'),
    path('product/<int:pk>/edit/', views.product_update, name='product_update'),
    
]