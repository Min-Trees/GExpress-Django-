from django.urls import path
from .views import register, user_login ,account_baking, guest , profile, total_order, body , location_select , send_otp,verify_otp

urlpatterns = [
    path('signup/', register, name='signup'),
    path('login/', user_login, name='login'),
    path('payment/', account_baking, name='payment'),
    path('home/', guest, name='guest'),
    path('profile', profile, name='profile'),
    path('total_order/<uuid:user_id>/', total_order, name='total_order'),
    path('', body, name='home'),
    path('location/', location_select, name='location'),
    path('send_otp/', send_otp, name='send_otp'),
    path('verify_otp/', verify_otp, name='verify_otp'),

]