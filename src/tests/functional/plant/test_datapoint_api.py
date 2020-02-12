from tests.utils import APITest
from tests.factories import DataPointFactory


class DataPointAPITest(APITest):
    def setUp(self):
        super().setUp()
        self.num_datapoints = 9
        self.datapoint_list = [DataPointFactory() for _ in range(self.num_datapoints)]

    def test_datapoint_list(self):
        self.response = self.get("api_plant:datapoint-list")
        self.response.assertStatusEqual(200)
        self.assertEqual(len(self.response.body), self.num_datapoints)
