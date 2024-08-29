from django.urls import path
from . import views
urlpatterns = [
    path('',views.admin_order,name='order_list'),
    path('ordermanage/<int:id>',views.order_manage,name='order_manage'),
    path('change-order-status/<int:id>/<str:status>/', views.change_order_status, name='change_order_status'),
    path('invoice/<int:id>',views.invoice,name="invoice")
]