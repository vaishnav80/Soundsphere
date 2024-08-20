from django.urls import * 
from .  import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('',views.admin_login,name='admin_login'),
    path('admin_dashboard/',views.admin_dashboard,name='admin_dashboard'),
    path('user_details/',views.user_details,name='userdetails'),
    path('user_details/togle/<int:id>',views.toggle_status,name='toggle_status'),
    path('logout/',views.admin_logout,name='logout'),
    path('download/pdf-report/<str:date_range>/<str:start_date>/<str:end_date>', views.generate_pdf_report, name='generate_pdf_report'),
    path('downloadexcel/<str:date_range>/<str:start_date>/<str:end_date>',views.generate_excel_report,name="generate_excel_report")
]