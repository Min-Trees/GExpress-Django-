
from django.db import models
from django.utils import timezone
import uuid
from django.core.validators import MaxValueValidator
class Account(models.Model):
    CUSTOMER = 'Customer'
    SHOP = 'Shop'
    SHIPPER = 'Shipper'
    ROLE_CHOICES = [
        (CUSTOMER,'Customer'),
        (SHOP,'Shop'),
        (SHIPPER,'Shipper')
    ]
    user_id = models.UUIDField(primary_key=True,default=uuid.uuid4)
    user_name = models.CharField(max_length = 100)
    password = models.CharField(max_length = 20)
    email = models.EmailField(max_length = 200)
    phone = models.CharField(max_length = 12)
    address = models.CharField(max_length = 400)
    role = models.CharField(ROLE_CHOICES, default = CUSTOMER, max_length=10)
    def __str__(self): 
        return self.user_name , self.role
    
# Create your models here.
class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length = 400, unique = True)
    type = models.CharField(max_length = 40)
    quantity = models.IntegerField(default = 0)
    price = models.FloatField(default = 0)
    description = models.CharField(max_length = 1000, null = True)
    def __str__(self):
        return self.name

class Order(models.Model):
    order_id = models.UUIDField(primary_key = True,default=uuid.uuid4)
    id_customer = models.ForeignKey(Account, on_delete = models.CASCADE)
    id_product = models.ForeignKey(Product, on_delete = models.CASCADE)
    order_price = models.FloatField(default = 0)
    created_date = models.DateField(default=timezone.now)
    updated_date = models.DateField(default=timezone.now)
    def __str__(self):
        return f'{self.order_id} - {self.id_product.name}'


class TransportByEcm(models.Model):
    
    CREATE = 'Create'
    MOVING = 'Moving'
    FINISH = 'Finish'
    Status_choices =[
    (CREATE,'Create'),
    (MOVING, 'Moving'),
    (FINISH,'Finish')
    ]
    
    default_shipping = 15000
    
    from_district = models.CharField(max_length=200, null=True, blank=True)
    from_province = models.CharField(max_length=200, null=True, blank=True)

    to_district = models.CharField(max_length=200, null=True, blank=True)
    to_province = models.CharField(max_length=200, null=True, blank=True)
    
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name_product = models.CharField(max_length = 400)
    weigth = models.FloatField(null = False, default = 0)
    from_send = models.CharField(max_length = 2000 ,null = False,default="")
    to_send = models.CharField(max_length = 2000 ,null = False,default="")
    transport_price = models.FloatField(default = default_shipping)
    created_date = models.DateField(default=timezone.now)
    updated_date = models.DateField(default=timezone.now)
    
    def __str__(self):
        return self.id , self.name_product
    
class Transport(models.Model):
    CREATE = 'Create'
    MOVING = 'Moving'
    FINISH = 'Finish'
    Status_choices =[
    (CREATE,'Create'),
    (MOVING, 'Moving'),
    (FINISH,'Finish')
    ]
    
    default_shipping = 15000
    
    from_district = models.CharField(max_length=200, null=True, blank=True)
    from_province = models.CharField(max_length=200, null=True, blank=True)

    to_district = models.CharField(max_length=200, null=True, blank=True)
    to_province = models.CharField(max_length=200, null=True, blank=True)

    transport_id = models.UUIDField(primary_key = True)
    id_customer = models.ForeignKey(Account, on_delete = models.CASCADE)
    id_product = models.ForeignKey(Product, on_delete = models.CASCADE)
    weigth = models.FloatField(null = False, default = 0)
    from_send = models.CharField(max_length = 2000 ,null = False,default="")
    to_send = models.CharField(max_length = 2000 ,null = False,default="")
    transport_price = models.FloatField(default = default_shipping)
    created_date = models.DateField(default=timezone.now)
    updated_date = models.DateField(default=timezone.now)
    
    # transport_price different address
    def save(self,*args, **kwargs):
        addresses_are_different = (
        self.from_district != self.to_district or
        self.from_province != self.to_province
        )

        self.from_send = f"{self.from_district}, {self.from_province}"
        self.to_send = f"{self.to_district}, {self.to_province}"
    
        if addresses_are_different:
            self.transport_price = 35000
        super().save(*args, **kwargs)
    def __str__(self):
        return self.transport_id
#tk transportdjango
class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    account_pay = models.CharField(max_length=20, null=False,   default='123456789')
    account_name = models.CharField(max_length=100, null=False, default='Nguyen Van A')
    cvv_pay = models.IntegerField(max_length=3, null=False, default='123')
    expiration_month = models.IntegerField(max_length=2, null=False, default='12')
    expiration_year = models.IntegerField(max_length=4, null=False, default='2024')  
    created_date = models.DateField(default=timezone.now)
    updated_date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.account_name
    
class Payments(models.Model):
    pass