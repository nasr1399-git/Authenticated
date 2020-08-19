from django.urls import path , include
from ways.views import *

urlpatterns = [
    path('', home,name='home'),
    path('logout/',log_out,name='logout'),
    path('login/',log_in,name='login'),
    path('bfa/',loginBFA, name = 'bfa'), 
    path('otp/',loginOTP, name = 'otp'),
    path('signup/',sign_up,name='signup'),
    path('signup/back/',back,name='back home'),

]
