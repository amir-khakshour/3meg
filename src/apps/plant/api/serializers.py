from rest_framework import serializers
from django.conf import settings
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


class DataPointUpdateSerializer(serializers.Serializer):
    after = serializers.DateField(format=settings.DATAPOINT_DATE_FILTER_FORMAT,
                                  input_formats=[settings.DATAPOINT_DATE_FILTER_FORMAT, 'iso-8601'], required=True)
    before = serializers.DateField(format=settings.DATAPOINT_DATE_FILTER_FORMAT,
                                   input_formats=[settings.DATAPOINT_DATE_FILTER_FORMAT, 'iso-8601'], required=True)

    class Meta:
        fields = ('after', 'before',)
