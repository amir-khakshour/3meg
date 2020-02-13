import datetime
from django.conf import settings
from django.utils.timezone import make_aware

def prepare_json_datapoint_for_save(plant_id, datapoint):
    """
    Convert a json formatted datapoint from monitoring endpoint to the
    datapoint dictionary ready for being saved in DB
    - TODO: use DRF serializer to validate input datapoint and use it's validated data to save
    - datapoint format:
    {
        "datetime": "2019-01-01T00:00:00",
        "expected": {
            "energy": 64.57977569815803,
            "irradiation": 99.63686683621316
        },
        "observed": {
            "energy": 96.67850486850264,
            "irradiation": 75.79305476577491
        }
    }
    :param plant:
    :param datapoint:
    :return:
    """
    dt = datetime.datetime.strptime(datapoint['datetime'], settings.DATAPOINT_DATETIME_FORMAT)
    return {
        'plant_id': plant_id,
        'energy_expected': datapoint['expected']['energy'],
        'energy_observed': datapoint['observed']['energy'],
        'irradiation_expected': datapoint['expected']['irradiation'],
        'irradiation_observed': datapoint['observed']['irradiation'],
        'datetime': make_aware(dt),
    }
