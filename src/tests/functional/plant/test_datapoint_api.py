import datetime
import random

from django.db.models import Count, Max, Min
from django.urls import reverse
from django.utils.timezone import make_naive

from plant.models import DataPoint
from tests.factories import DataPointFactory
from tests.utils import APITest


class DataPointAPITest(APITest):
    def setUp(self):
        super().setUp()
        self.num_datapoints = 9
        self.datapoint_list = [DataPointFactory() for _ in range(self.num_datapoints)]
        self.agg_datapoints_by_date = DataPoint.objects.extra(select={'date': 'date( datetime )'}) \
            .values('date') \
            .annotate(total_datapoints=Count('plant_id')).order_by('date')

    def test_datapoint_list(self):
        self.response = self.get("api_plant:datapoint-list")
        self.response.assertStatusEqual(200)
        self.assertIsNotNone(self.response.body)
        self.assertEqual(self.response.body['count'], self.num_datapoints)

    def test_datapoint_filter_range(self):
        agg = DataPoint.objects.aggregate(datetime__min=Min('datetime'),
                                          datetime__max=Max('datetime'), count=Count('id'))

        # add one second to make the border more proper
        datetime__min = make_naive(agg['datetime__min'] - datetime.timedelta(seconds=1)).strftime('%Y-%m-%d %H:%M:%S')
        datetime__max = make_naive(agg['datetime__max'] + datetime.timedelta(seconds=1)).strftime('%Y-%m-%d %H:%M:%S')

        # Filter no item
        self.response = self.client.get(reverse("api_plant:datapoint-list", kwargs={'version': 1}),
                                        {'datetime__gte': datetime__min,
                                         'datetime__lte': datetime__max})

        self.response.assertStatusEqual(200)
        self.assertEqual(self.response.body['count'], agg['count'])

        # Filter all data
        self.response = self.client.get(reverse("api_plant:datapoint-list", kwargs={'version': 1}),
                                        {'datetime__lt': datetime__min,
                                         'datetime__gt': datetime__max})

        self.response.assertStatusEqual(200)
        self.assertEqual(self.response.body['count'], 0)

    def test_datapoint_filter_exact_date(self):
        """"
        Since we have more than one DataPoints so we can use the total
        number of DataPoints in a day and check it against the API endpoint
        """
        agg = sorted(self.agg_datapoints_by_date, key=lambda item: item['total_datapoints'])
        high_volume_item = agg[0]  # get item with the least amount of DataPoints in the date

        self.response = self.client.get(
            reverse("api_plant:datapoint-list", kwargs={'version': 1}), {'date_exact': high_volume_item['date'], }
        )

        self.response.assertStatusEqual(200)
        self.assertEqual(self.response.body['count'], high_volume_item['total_datapoints'])

    def test_datapoint_filter_date_range(self):
        agg = list(self.agg_datapoints_by_date)

        # get random Item from list
        random_index = random.randrange(0, len(agg))
        random_item = agg[random_index]
        total_datapoints_to_item = sum([item['total_datapoints'] for item in agg[:random_index]])
        self.response = self.client.get(
            reverse("api_plant:datapoint-list", kwargs={'version': 1}), {'date_before': random_item['date'], }
        )

        self.response.assertStatusEqual(200)
        self.assertEqual(self.response.body['count'], total_datapoints_to_item)
