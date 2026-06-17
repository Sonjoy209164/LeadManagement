from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AssignedWorkViewSet, LeadViewSet, TeamLeadViewSet, dashboard

router = DefaultRouter()
router.register("team-leads", TeamLeadViewSet, basename="team-lead")
router.register("assigned-work", AssignedWorkViewSet, basename="assigned-work")
router.register("leads", LeadViewSet, basename="lead")

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("api/", include(router.urls)),
]
