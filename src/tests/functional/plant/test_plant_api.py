from tests.utils import APITest
from tests.factories import PlantFactory


class CategoryTest(APITest):
    def setUp(self):
        super().setUp()
        self.num_plants = 4
        self.plants_list = [PlantFactory() for _ in range(self.num_plants)]

    def test_plant_list(self):
        self.response = self.get("api_plant:plant-list")
        self.response.assertStatusEqual(200)
        self.assertEqual(len(self.response.body), self.num_plants)
