from rest_framework.routers import DefaultRouter 

from bots.views.bot_view import BotViewSet

router = DefaultRouter()
router.register(r"", BotViewSet, basename="bots")

urlpatterns = router.urls