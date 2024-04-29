from rest_framework.routers import DefaultRouter

from core.views import *

router = DefaultRouter()
router.register('vendors', VendorsViewset)
router.register('purchase_orders', PurchaseOrderViewset)

urlpatterns = [

] + router.urls