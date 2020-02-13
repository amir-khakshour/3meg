import logging
import requests
from celery import shared_task
from django.conf import settings
logger = logging.getLogger(__file__)


@shared_task
def datapoints_update(plant_id, after_date, before_date):
    """
    Task to Update datapoints of a Plant based on date filter
    :param plant_id: plant primary key to update it's datapoints
    :param after_date: Start date in the format of settings.DATAPOINT_DATE_FILTER_FORMAT
    :param before_date: End date in the format of settings.DATAPOINT_DATE_FILTER_FORMAT
    :return:
    """
    from plant.models import Plant
    try:
        plant = Plant.objects.get(pk=plant_id)
        url = settings.DATAPOINT_FETCH_URL_FORMAT.format(plant.source_id, after_date, before_date)
        response = requests.get(url)
    except Exception as e:  # TODO add more granularity to exception handling
        msg = str(e)
        logger.error(msg, exc_info=True)
