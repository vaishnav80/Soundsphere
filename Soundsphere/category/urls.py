from django.urls import path

from . import views

urlpatterns = [
    path('',views.category,name='category'),
    path('types/',views.types,name='types'),
    path('brand/',views.brand,name='brand'),
    path('connection/',views.connection,name='connection'),
    path('brand_details/togle/<int:id>',views.brand_status,name='brand_status'),
    path('connection_details/togle/<int:id>',views.connection_status,name='connection_status'),
    path('type_details/togle/<int:id>',views.type_status,name='type_status'),
    path('addtype/',views.addtypes,name='addtype'),
    path('addconnection/',views.addconnection,name='addconnection'),
    path('addbrand/',views.addbrand,name='addbrand'),
]