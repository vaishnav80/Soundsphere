from django.urls import path
from . import views
urlpatterns = [
    path('',views.shop,name='shop'),
    path('shop/<int:id>',views.shop,name='shopid'),
    path('details/<int:id>',views.product_details,name='details'),
    path('search/',views.search,name='search')
]