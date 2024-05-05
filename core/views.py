from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token

from core.models import *
from core.serializers import VendorSerializer, PurchaseOrderSerializer, UserSerializer

# Create your views here.
class LoginView(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        # Your authentication logic here
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=401)


class VendorsViewset(ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticated,]
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
    permission_classes = [IsAuthenticated,]
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