from django.contrib import admin

from .models import AssignedWork, Lead, TeamLead


@admin.register(TeamLead)
class TeamLeadAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "email",
        "department",
        "designation",
        "specialization",
        "status",
    )
    list_filter = ("status", "department", "specialization")
    search_fields = ("full_name", "email", "phone", "department", "specialization")


@admin.register(AssignedWork)
class AssignedWorkAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "team_lead",
        "client_name",
        "campaign_name",
        "channel",
        "status",
        "progress",
        "due_date",
    )
    list_filter = ("status", "priority", "campaign_type", "channel")
    search_fields = ("title", "client_name", "campaign_name", "team_lead__full_name")


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "company_name",
        "industry",
        "source",
        "assigned_to",
        "status",
        "lead_score",
        "lead_grade",
    )
    list_filter = ("lead_grade", "status", "source", "industry")
    search_fields = ("full_name", "email", "phone", "company_name", "industry")
    readonly_fields = ("lead_score", "lead_grade")
