from django.urls import path
from .views import Price, create, info, Search_Transport , manager , info_transport , home

urlpatterns = [
    path('transportprice', Price, name='transportprice'),
    path('create',  create, name='create'),
    path('info',info, name='info_order'),
    path('search_transport/', Search_Transport, name='search_transport'),
    path('manager', manager, name='manager'),
    path('info_transport/', info_transport, name='info_transport'),
    path('home', home, name='home'),
]