from django.urls import path
from .views import Price

urlpatterns = [
    path('transportprice', Price, name='transportprice')
]