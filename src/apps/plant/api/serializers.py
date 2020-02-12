from rest_framework import serializers

from ..models import Plant, DataPoint


class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = '__all__'


class DataPointSerializer(serializers.ModelSerializer):
    date_created = serializers.DateTimeField(read_only=True)

    class Meta:
        model = DataPoint
        fields = '__all__'
