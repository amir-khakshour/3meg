from rest_framework.viewsets import GenericViewSet

from plant.drf.utils import override_serializer


class DummySerializer(object):
    pass


def test_override_serializer():
    view = GenericViewSet()
    with override_serializer(view, DummySerializer):
        assert view.get_serializer_class() == DummySerializer
