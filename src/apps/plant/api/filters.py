import django_filters

from ..models import DataPoint


class DataPointFilter(django_filters.FilterSet):
    """Filter for DataPoints by date"""
    date = django_filters.DateFilter(field_name='datetime', method='filter_date')

    def filter_date(self, queryset, name, value):
        # construct the full lookup expression.
        lookup = '__'.join([name, 'date'])
        return queryset.filter(**{lookup: value})

    class Meta:
        model = DataPoint
        fields = {
            'datetime': ['exact', 'lt', 'gt', 'lte', 'gte'],
        }
