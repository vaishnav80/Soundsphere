from django.urls import *
from . import views
urlpatterns = [
    path('',views.Home,name='home'),
    path('signin/<int:id>',views.signin,name='signin'),
    path("signout/",views.signout,name='signout'),
    path('signup/',views.signup,name='signup'),
    path('otp-verification/', views.otp_verification_view, name='otp_verification'),
    path('forgot/',views.forgot_password,name='forgotpassword'),
    path('forgot_verfication/',views.otp_verification_forgotpassword,name='forgot_otpverification'),
    path('resetpassword/',views.reset_password,name='resetpassword'),
    path('refferal_code',views.refferal_code,name='refferal_code'),
    path('regenerate_otp/<int:id>',views.regenerate_otp,name='regenerate_otp'),
]