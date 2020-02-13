import pytest
from unittest.mock import Mock, patch
from tests.factories import PlantFactory
from plant.tasks import datapoints_update
from plant.models import DataPoint


@pytest.mark.django_db
@patch('plant.tasks.requests.get')
def test_datapoints_update(mock_get):
    """
    Test if after calling datapoints_update, the related datapoints get inserted to the database
    :param mock_get: Mocked requests.get function
    :return:
    """
    plant = PlantFactory()
    datapoints = [{"datetime": "2020-01-01T00:00:00",
                   "expected": {"energy": 56.02760101729767, "irradiation": 5.053311239838092},
                   "observed": {"energy": 48.51819791737828, "irradiation": 66.78311981258118}},
                  {"datetime": "2020-01-01T01:00:00",
                   "expected": {"energy": 40.77808991181146, "irradiation": 95.23817534518328},
                   "observed": {"energy": 37.68257746073339, "irradiation": 52.34537793795987}},
                  {"datetime": "2020-01-01T02:00:00",
                   "expected": {"energy": 8.179597201672234, "irradiation": 6.269232971177307},
                   "observed": {"energy": 93.5759301703764, "irradiation": 42.038912585036265}}]

    mock_get.return_value = Mock(ok=True)
    mock_get.return_value.json.return_value = datapoints
    datapoints_update(plant.pk, '2020-01-01', '2020-01-02')  # Run the task synchronously
    # Test Database against number of added datapoints
    assert DataPoint.objects.filter(plant=plant).count() == len(datapoints)
