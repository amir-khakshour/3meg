from rest_framework import routers

from .views import (
    PlantViewSet,
)

app_name = 'api_plant'
router = routers.DefaultRouter()
router.register(r'plant', PlantViewSet)

urlpatterns = router.urls
