from django.urls import path
from . import views
urlpatterns = [
    path('admin_review/',views.admin_review,name="admin_review"),
    path('user_review/',views.user_review,name="user_review"),
    path('add_review/<str:id>',views.add_review,name="add_review"),
    path('delete_review/<int:id>/<int:id2>',views.delete_review,name="delete_review")
]