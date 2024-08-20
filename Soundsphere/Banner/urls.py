from django.urls import path
from . import views

urlpatterns = [
    path('',views.banner,name='banner'),
    path('addbanner/',views.addbanner,name='addbanner'),
    path('deletebaanner/<int:id>',views.delete_banner,name='deletebanner')
]