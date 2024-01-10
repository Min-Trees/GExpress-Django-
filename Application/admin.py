from django.contrib import admin
from .models import Account , Product , Payments , Payment
# Register your models here.
admin.site.register(Account)
admin.site.register(Product)
admin.site.register(Payment)
admin.site.register(Payments)