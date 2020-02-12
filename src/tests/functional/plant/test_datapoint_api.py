import datetime

from django.urls import reverse
from django.db.models import Min, Max, Count
from django.utils.timezone import make_naive

from tests.utils import APITest
from tests.factories import DataPointFactory
from plant.models import DataPoint


class DataPointAPITest(APITest):
    def setUp(self):
        super().setUp()
        self.num_datapoints = 9
        self.datapoint_list = [DataPointFactory() for _ in range(self.num_datapoints)]

    def test_datapoint_list(self):
        self.response = self.get("api_plant:datapoint-list")
        self.response.assertStatusEqual(200)
        self.assertEqual(len(self.response.body), self.num_datapoints)

    def test_datapoint_filter(self):
        agg = DataPoint.objects.aggregate(datetime__min=Min('datetime'), datetime__max=Max('datetime'), count=Count('id'))

        # add one second to make the border more proper
        datetime__min = make_naive(agg['datetime__min'] - datetime.timedelta(seconds=1)).strftime('%Y-%m-%d %H:%M:%S')
        datetime__max = make_naive(agg['datetime__max'] + datetime.timedelta(seconds=1)).strftime('%Y-%m-%d %H:%M:%S')

        # Filter no item
        self.response = self.client.get(reverse("api_plant:datapoint-list", kwargs={'version': 1}),
                                        {'datetime__gte': datetime__min,
                                         'datetime__lte': datetime__max})

        self.response.assertStatusEqual(200)
        self.assertEqual(len(self.response.body), agg['count'])

        # Filter all data
        self.response = self.client.get(reverse("api_plant:datapoint-list", kwargs={'version': 1}),
                                        {'datetime__lt': datetime__min,
                                         'datetime__gt': datetime__max})

        self.response.assertStatusEqual(200)
        self.assertEqual(len(self.response.body), 0)
