from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from django_filters import rest_framework as filters

from ..models import Plant, DataPoint
from ..drf.utils import override_serializer
from .serializers import PlantSerializer, DataPointSerializer, DataPointUpdateSerializer
from .filters import DataPointFilter


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
                return Response(status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DataPointViewSet(viewsets.ModelViewSet):
    queryset = DataPoint.objects.all()
    serializer_class = DataPointSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter,)
    filterset_class = DataPointFilter
