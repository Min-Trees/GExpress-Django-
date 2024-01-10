from django.db import models
from django.utils import timezone
import uuid
import secrets

def default_expected_date():
    return timezone.now() + timezone.timedelta(days=3)

class TranSport_API(models.Model):
    #default evariable
    default_shipping = 15000
    
    transport_id = models.UUIDField(primary_key = True , default = uuid.uuid4, null = False)
    transprot_code = models.CharField(max_length = 16, default = secrets.token_hex(8), null = False)
    transport_name = models.CharField(max_length = 2000, null = False, default = "")
    transport_price = models.FloatField(default = default_shipping)
    weight = models.FloatField(null = False, default = 0)
    quantity = models.IntegerField(null = False, default = 0)
    name_ownerShop = models.CharField(max_length = 200 , null = False , default = "")
    name_customer = models.CharField(max_length = 200 , null = False , default = "")
    description = models.CharField(max_length = 2000 , null = True , default = "")
    customer_phone = models.CharField(max_length = 20 , null = False , default = "")
    from_district = models.CharField(max_length=200, null=False, blank=True)
    from_province = models.CharField(max_length=200, null=False, blank=True)
    to_district = models.CharField(max_length=200, null=False, blank=True)
    to_province = models.CharField(max_length=200, null=False, blank=True)
    # list of post office( post office of sender and receiver) inserted 
    post_offices = models.CharField(max_length = 2000 , null = False , default = "")
    #calculate the expected date of delivery
    expected_date = models.DateField(default=default_expected_date)
    created_at = models.DateField(default=timezone.now)
    updated_at = models.DateField(default=timezone.now)