
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import uuid
from django.core.validators import MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import secrets
from django.views.decorators.csrf import csrf_exempt

class AccountManager(BaseUserManager):
    def create_user(self, user_name, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        user = self.model(user_name=user_name, email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_name, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(user_name, email, password, **extra_fields)

class Account(AbstractBaseUser, PermissionsMixin):

    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=200, unique=True)
    phone = models.CharField(max_length=12, blank=True)
    

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = AccountManager()

    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['email']

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name='account_groups'
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='account_user_permissions'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_name

    class Meta:
        ordering = ['-created_at']

class CustomUser(Account):
    # Bất kỳ trường hoặc phương thức tùy chỉnh nào bạn muốn thêm vào CustomUser
    # có thể được thêm ở đây
    pass
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
class Total_Order(models.Model):
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    id_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_price = models.FloatField(default=0)
    user_name = models.CharField(max_length=100, blank=True, null=True)
    
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
    cvv_pay = models.IntegerField( null=False, default='123')
    expiration_month = models.IntegerField( null=False, default='12')
    expiration_year = models.IntegerField(null=False, default='2024')  
    created_date = models.DateField(default=timezone.now)
    updated_date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.account_name
    
class Payments(models.Model):
    pass

class Province(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class District(models.Model):
    name = models.CharField(max_length=100)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

