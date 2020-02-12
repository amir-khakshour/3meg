import django_filters

from ..models import DataPoint


class DataPointFilter(django_filters.FilterSet):
    class Meta:
        model = DataPoint
        fields = {
            'datetime': ['exact', 'lt', 'gt', 'lte', 'gte'],
        }
