from django.urls import path
from . import views

urlpatterns = [
    path('wallet/',views.wallet,name='wallet'),
    # path('get_coordinates/',views.get_coordinates,name='get_coordinates')
]