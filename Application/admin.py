from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account , Product , Payments , Payment, Total_Order, Order , CustomUser
admin.site.register(Account)
admin.site.register(Product)
admin.site.register(Payment)
admin.site.register(Payments)
admin.site.register(Total_Order)
admin.site.register(Order)
