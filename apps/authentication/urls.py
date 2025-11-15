# apps/authentication/urls.py

from django.urls import path

from apps.authentication.view.admin_view import changePassword, changePasswordSuperadmin
from .views import login, register, enviarOTP, validarOTP, resendOTP, getCountry, getProvince, onboarding, updatePassword, validarEmail
from apps.authentication.view.superadmin_view import loginSuperadmin

urlpatterns = [
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('sendOTP/', enviarOTP, name='enviarotp'),
    path('validateOTP/', validarOTP, name='validarotp'),
    path('resendOTP/', resendOTP, name='resendotp'),
    path('getCountry/', getCountry, name='getcountry'),
    path('getProvince/', getProvince, name='getprovince'),
    path('onboarding/', onboarding, name='getprovince'),
    path('updatePassword/', updatePassword, name='reset-password'),
    path('validateEmail/', validarEmail, name='validarEmail'),
    path('superadmin/loginsuperadmin/', loginSuperadmin, name='login_superadmin'),
    path('dashboard/changepassword/', changePassword,
         name='change_password_admin'),
    path('dashboard/changepassuperadmin/', changePasswordSuperadmin,
         name='change_password_admin_pk'),
]