from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from core.models import *
from core.serializers import VendorSerializer, PurchaseOrderSerializer

# Create your views here.
class VendorsViewset(ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [AllowAny,]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = []
    search_fields = []
    ordering_fields = []
    pagination_class  = PageNumberPagination

    @action(detail=True, methods=['get'])
    def performance(self, request, pk=None):
        instance = self.get_object()
        serializer_data = self.serializer_class(instance).data
        return Response(data=serializer_data, status=status.HTTP_200_OK)


class PurchaseOrderViewset(ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    permission_classes = []
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = []
    search_fields = []
    ordering_fields = []
    pagination_class  = PageNumberPagination

    @action(detail=True, methods=['put'])
    def acknowledge(self, request, pk=None):
        instance = self.get_object()
        if request.data.get('acknowledgment_date', None) is None:
            return Response({'error': 'Acknowledgement Date cannot be empty'}, status=status.HTTP_400_BAD_REQUEST)

        instance.acknowledgment_date = request.data.get('acknowledgment_date')
        instance.save()

        return Response({'details': 'Acknowledgement Updated', 'data': self.serializer_class(instance).data}, status=status.HTTP_200_OK)