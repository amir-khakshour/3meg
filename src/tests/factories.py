import datetime
import factory
from factory import fuzzy
from django.utils import timezone
from django.contrib.auth import get_user_model

from plant.models import Plant, DataPoint


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    first_name = factory.Sequence(lambda n: "User %03d" % n)
    username = factory.Sequence(lambda n: "user_%d" % n)
    email = factory.Sequence(lambda n: "user_%d@example.com" % n)


class PlantFactory(factory.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'Plant %d' % n)

    class Meta:
        model = Plant


class DataPointFactory(factory.DjangoModelFactory):
    class Meta:
        model = DataPoint

    plant = factory.SubFactory(PlantFactory)
    energy_expected = fuzzy.FuzzyDecimal(0.1111111, 80.11111111)
    energy_observed = fuzzy.FuzzyDecimal(0.1111111, 80.11111111)
    irradiation_expected = fuzzy.FuzzyDecimal(0.1111111, 80.11111111)
    irradiation_observed = fuzzy.FuzzyDecimal(0.1111111, 80.11111111)
    datetime = fuzzy.FuzzyDateTime(timezone.now() - datetime.timedelta(days=10))
