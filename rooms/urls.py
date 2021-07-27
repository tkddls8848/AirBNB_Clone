from rest_framework.routers import DefaultRouter
from . import views

app_name = "rooms"
router = DefaultRouter()
router.register("", views.RoomSet)

urlpatterns = router.urls
