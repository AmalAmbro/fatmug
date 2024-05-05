from django.contrib.auth.models import User

from rest_framework.serializers import ModelSerializer
from core.models import *


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)
        
class VendorSerializer(ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'

class PurchaseOrderSerializer(ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'