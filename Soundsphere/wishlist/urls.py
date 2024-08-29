from django.urls import *
from . import views

urlpatterns = [
    path('',views.wish,name='wishlist'),
    path('add_to_wishlist/',views.add_to_wishlist,name='add_to_wishlist'),
    path('remove_wish/<int:id>',views.wish_remove,name='wish_remove'),
]