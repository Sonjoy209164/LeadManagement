from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework import viewsets

from .models import AssignedWork, TeamLead
from .serializers import AssignedWorkSerializer, TeamLeadSerializer


@login_required
def dashboard(request):
    return render(request, "leads/dashboard.html")


class TeamLeadViewSet(viewsets.ModelViewSet):
    serializer_class = TeamLeadSerializer
    queryset = TeamLead.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params
        search = params.get("search", "").strip()

        if search:
            queryset = queryset.filter(
                Q(full_name__icontains=search)
                | Q(email__icontains=search)
                | Q(phone__icontains=search)
                | Q(department__icontains=search)
                | Q(designation__icontains=search)
                | Q(specialization__icontains=search)
            )

        for field in ("status", "department"):
            value = params.get(field)
            if value:
                queryset = queryset.filter(**{field: value})

        return queryset


class AssignedWorkViewSet(viewsets.ModelViewSet):
    serializer_class = AssignedWorkSerializer
    queryset = AssignedWork.objects.select_related("team_lead")

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params
        search = params.get("search", "").strip()

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search)
                | Q(client_name__icontains=search)
                | Q(campaign_name__icontains=search)
                | Q(responsibility__icontains=search)
                | Q(team_lead__full_name__icontains=search)
            )

        for field in ("team_lead", "status", "priority", "campaign_type", "channel"):
            value = params.get(field)
            if value:
                queryset = queryset.filter(**{field: value})

        return queryset
