from rest_framework import serializers
from .models import  Transport ,Order

class Serializers_Order(serializers.ModelSerializer):
    class Meta:
        models = Order
        field = '__all__'

class Serializers_Transprot(serializers.ModelSerializer):
    class Meta:
        models = Transport
        field = '__all__'
        
class Serializers_Transprot_By_Ecm(serializers.ModelSerializer):
    class Meta:
        models = Transport
        field = '__all__'