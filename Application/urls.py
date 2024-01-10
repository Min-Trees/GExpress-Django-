from django.urls import path
from .views import register, user_login ,account_baking

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('payment/', account_baking, name='payment'),
    
]