import datetime
import logging

import requests
from celery import shared_task
from celery.task import task
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from django.utils.timezone import make_naive

from .utils import prepare_json_datapoint_for_save

logger = logging.getLogger(__file__)


@shared_task
def datapoints_update(plant_id, after_date, before_date):
    """
    Task to Update datapoints of a Plant based on date filter
    - TODO: make the datetime of each datapoint timezone aware
    :param integer plant_id:
        plant primary key to update it's datapoints
    :param date_string after_date:
        Start date in the format of settings.DATAPOINT_DATE_FILTER_FORMAT
    :param date_string before_date:
        End date in the format of settings.DATAPOINT_DATE_FILTER_FORMAT
    :return:
    """
    from plant.models import Plant, DataPoint

    try:
        plant = Plant.objects.get(pk=plant_id)
        url = settings.DATAPOINT_FETCH_URL.format(plant.source_id, after_date, before_date)
        response = requests.get(url)
        data = response.json()
        if data and 'error' not in data:
            with transaction.atomic():
                DataPoint.objects.bulk_create([
                    DataPoint(**prepare_json_datapoint_for_save(plant.pk, item)) for item in data
                ])

    except Exception as e:  # TODO add more granularity to exception handling
        msg = str(e)
        logger.error(msg, exc_info=True)


@task
def auto_pull_plant_datapoints():
    """
    Pull data for each plant based on hourly range
    :return:
    """
    from plant.models import Plant

    now = make_naive(timezone.now())
    date_from = now.strftime('%Y-%m-%d %H:00:00')
    date_to = (now + datetime.timedelta(hours=1)).strftime('%Y-%m-%d %H:00:00')
    for plant_pk in Plant.objects.values_list('pk', flat=True):
        datapoints_update.delay(plant_pk, date_from, date_to)
