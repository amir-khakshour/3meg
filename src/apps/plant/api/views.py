from django_filters import rest_framework as filters
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from ..drf.utils import override_serializer
from ..models import DataPoint, Plant
from ..tasks import datapoints_update
from .filters import DataPointFilter
from .serializers import (
    DataPointSerializer, DataPointUpdateSerializer, PlantSerializer)


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

    @action(detail=True, methods=['post'])
    def datapoints_update(self, request, pk, version=1):
        # We can use a serializer for validating input dates too but it's not necessary here
        with override_serializer(self, DataPointUpdateSerializer):
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                # object = self.get_object()
                datapoints_update.delay(pk, after_date=serializer.data['after'], before_date=serializer.data['before'])
                return Response(data={'success': True, 'message': 'DataPoints pulling in process!'},
                                status=status.HTTP_202_ACCEPTED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DataPointViewSet(viewsets.ModelViewSet):
    queryset = DataPoint.objects.all()
    serializer_class = DataPointSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter,)
    filterset_class = DataPointFilter
