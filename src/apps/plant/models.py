from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import date as date_filter


class Plant(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("name"))
    source_id = models.PositiveIntegerField(verbose_name=_("Source Plant ID"))

    class Meta:
        verbose_name = _('Plant')
        verbose_name_plural = _('Plants')

    def __str__(self):
        return self.name


class DataPoint(models.Model):
    plant = models.ForeignKey('plant.Plant', on_delete=models.CASCADE)
    energy_expected = models.DecimalField(_("Expected Energy"), decimal_places=14, max_digits=20)
    energy_observed = models.DecimalField(_("Observed Energy"), decimal_places=14, max_digits=20)
    irradiation_expected = models.DecimalField(_("Expected Irradiation"), decimal_places=14, max_digits=20)
    irradiation_observed = models.DecimalField(_("Observed Irradiation"), decimal_places=14, max_digits=20)
    datetime = models.DateTimeField(_("datetime"), db_index=True)
    date_created = models.DateTimeField(_("Date updated"), auto_now=True, db_index=True)

    class Meta:
        ordering = ['-date_created']
        verbose_name = _('Data Point')
        verbose_name_plural = _('Data Points')

    def __str__(self):
        date_format = settings.DATAPOINT_DATE_FORMAT_FORMAT
        return 'DataPoint: plant=%s  datetime=%s ' % (self.plant, date_filter(self.datetime, date_format))
