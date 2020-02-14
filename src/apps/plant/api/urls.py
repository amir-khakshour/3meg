from rest_framework import routers

from .views import DataPointViewSet, PlantViewSet

app_name = 'api_plant'
router = routers.DefaultRouter()
router.register(r'plant', PlantViewSet)
router.register(r'datapoint', DataPointViewSet)

urlpatterns = router.urls
