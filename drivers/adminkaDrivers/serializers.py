from rest_framework import serializers
from .models import Publications, Driver, Cod

class PublicationsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Publications
        fields = ['driver', 'dataOfStartRoute', 'summ', 'allowed', 'text']

class DriversSerializers(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ['id','name', 'text', 'cod', 'telegramId']

class CodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cod
        fields = ['id', 'cod', 'stayt']