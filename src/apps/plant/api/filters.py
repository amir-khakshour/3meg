import django_filters

from ..models import DataPoint


class DataPointFilter(django_filters.FilterSet):
    """Filter for DataPoints by date"""
    date_exact = django_filters.DateFilter(field_name='datetime', method='filter_date_exact')
    date = django_filters.DateTimeFromToRangeFilter(field_name='datetime', method='filter_date_range')

    def filter_date_exact(self, queryset, name, value):
        # construct the full lookup expression.
        lookup = '__'.join([name, 'date'])
        return queryset.filter(**{lookup: value})

    def filter_date_range(self, queryset, name, value):
        # construct the full lookup expression.
        lookups = {}
        lookup = '__'.join([name, 'date'])
        date_after = value.start
        date_before = value.stop
        # date_step = value.step  # TODO apply step

        if date_after is not None:
            lookups['%s__gte' % lookup] = date_after
        if date_before is not None:
            lookups['%s__lt' % lookup] = date_before
        return queryset.filter(**lookups)

    class Meta:
        model = DataPoint
        fields = {
            'datetime': ['exact', 'lt', 'gt', 'lte', 'gte'],
        }
