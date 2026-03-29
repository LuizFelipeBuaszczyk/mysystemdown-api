from rest_framework.routers import DefaultRouter


from tenants.views.tenant_view import TenantView
from iam.views.membership_view import MembershipViewSet

router = DefaultRouter()
router.register(r"", TenantView, basename="tenants")
router.register("memberships", MembershipViewSet, basename="tenant-memberships")

urlpatterns = router.urls 