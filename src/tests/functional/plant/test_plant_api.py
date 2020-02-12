from tests.utils import APITest
from tests.factories import PlantFactory

from plant.models import DataPoint


class PlantAPITest(APITest):
    def setUp(self):
        super().setUp()
        self.num_plants = 4
        self.plants_list = [PlantFactory() for _ in range(self.num_plants)]

    def test_plant_list(self):
        self.response = self.get("api_plant:plant-list")
        self.response.assertStatusEqual(200)
        self.assertEqual(len(self.response.body), self.num_plants)

    def test_datapoints_in_plant(self):
        base_plant = self.plants_list[0]
        self.response = self.get("api_plant:plant-datapoints", url_kwargs={'pk': base_plant.pk})
        self.response.assertStatusEqual(200)

    def test_total_datapoints_in_category(self):
        base_plant = self.plants_list[0]
        self.response = self.get("api_goods:plant-datapoints", url_kwargs={'pk': base_plant.pk})
        num_datapoints_in_plant = DataPoint.objects.filter(plant_id=base_plant.pk).count()
        if self.response.body:
            self.assertEqual(len(self.response.body), num_datapoints_in_plant)
