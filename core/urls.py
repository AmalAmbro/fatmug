from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core.views import *

router = DefaultRouter()
router.register('vendors', VendorsViewset)
router.register('purchase_orders', PurchaseOrderViewset)

urlpatterns = [
    path('users/login/', LoginView.as_view())
] + router.urls