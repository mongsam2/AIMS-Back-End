from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import InappropriateReason

class ReasonsSerializer(ModelSerializer):
    class Meta:
        model = InappropriateReason
        exclude = ('document','id')