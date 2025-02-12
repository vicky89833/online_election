from django.urls import path
from . import views
urlpatterns = [
    path('get_otp/', views.otpGenerateView, name="get_otp"),
    path('verify_otp/', views.otpVarifyView, name="verify_otp"),
    path('voting/', views.votingView, name="voting"),
    path('admin/', views.AdminView, name="admin"),
]