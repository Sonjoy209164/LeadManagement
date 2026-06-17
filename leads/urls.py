from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AssignedWorkViewSet, TeamLeadViewSet, dashboard

router = DefaultRouter()
router.register("team-leads", TeamLeadViewSet, basename="team-lead")
router.register("assigned-work", AssignedWorkViewSet, basename="assigned-work")

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("api/", include(router.urls)),
]
