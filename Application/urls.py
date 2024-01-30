from django.urls import path
from .views import register, user_login ,account_baking, guest , profile, total_order

urlpatterns = [
    path('signup/', register, name='signup'),
    path('login/', user_login, name='login'),
    path('payment/', account_baking, name='payment'),
    path('', guest, name='guest'),
    path('profile', profile, name='profile'),
    path('total_order/<uuid:user_id>/', total_order, name='total_order'),
]