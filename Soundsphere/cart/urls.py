from django.urls import path
from . import views

urlpatterns = [
    path('',views.cart,name='cart'),
    path('remove/<int:id>',views.remove,name='remove'),
    path('update-quantity-ajax/', views.update_quantity_ajax, name='update_quantity_ajax'),
    
]