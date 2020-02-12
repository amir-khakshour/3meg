from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import Plant, DataPoint
from ..drf.utils import override_serializer
from .serializers import PlantSerializer, DataPointSerializer


class PlantViewSet(viewsets.ModelViewSet):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer

    @action(detail=True, methods=['get'])
    def datapoints(self, request, pk, version=1):
        products = DataPoint.objects.filter(plant_id=pk)
        page = self.paginate_queryset(products)
        with override_serializer(self, DataPointSerializer):
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)


class DataPointViewSet(viewsets.ModelViewSet):
    queryset = DataPoint.objects.all()
    serializer_class = DataPointSerializer
