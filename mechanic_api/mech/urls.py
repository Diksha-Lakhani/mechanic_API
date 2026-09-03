from rest_framework.routers import DefaultRouter
from .views import MechanicViewSet, ServiceRequestViewSet

#creates routes to be hit while making requests
#for example: for mechanics, 
# get route is /mechanics/ (for all) and /mechanics/{id} (for specific)
# post route is /mechanics/ (for adding new mechanic)
# put/patch/delete is /serbice-request/{id} (for full update /partial update/delete of specific mechanic)
router = DefaultRouter()
router.register(r'mechanics', MechanicViewSet, basename='mechanic')
router.register(r'service-requests', ServiceRequestViewSet, basename='servicerequest')

urlpatterns = router.urls