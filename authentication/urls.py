from django.urls import path
from authentication import views

urlpatterns = [
    path('register/', views.register, name='register'), 
      path('request-otp/', views.request_otp, name='request_otp'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
 path('protected/', views.protected_view, name='verify_otp'),
]   

