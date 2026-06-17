from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class TeamLead(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"
        ON_LEAVE = "on_leave", "On Leave"

    full_name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=30, blank=True)
    department = models.CharField(max_length=120)
    designation = models.CharField(max_length=120, default="Marketing Team Lead")
    specialization = models.CharField(max_length=120, blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["full_name"]

    def __str__(self):
        return self.full_name


class AssignedWork(models.Model):
    class CampaignType(models.TextChoices):
        SEO = "seo", "SEO"
        SOCIAL_MEDIA = "social_media", "Social Media"
        PAID_ADS = "paid_ads", "Paid Ads"
        EMAIL = "email", "Email"
        CONTENT = "content", "Content"
        EVENT = "event", "Event"
        BRAND_AWARENESS = "brand_awareness", "Brand Awareness"
        LEAD_GENERATION = "lead_generation", "Lead Generation"

    class Channel(models.TextChoices):
        FACEBOOK = "facebook", "Facebook"
        INSTAGRAM = "instagram", "Instagram"
        GOOGLE_ADS = "google_ads", "Google Ads"
        LINKEDIN = "linkedin", "LinkedIn"
        EMAIL = "email", "Email"
        WEBSITE = "website", "Website"
        YOUTUBE = "youtube", "YouTube"
        OFFLINE_EVENT = "offline_event", "Offline Event"

    class WorkStatus(models.TextChoices):
        NOT_STARTED = "not_started", "Not Started"
        IN_PROGRESS = "in_progress", "In Progress"
        BLOCKED = "blocked", "Blocked"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    class Priority(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"
        URGENT = "urgent", "Urgent"

    team_lead = models.ForeignKey(
        TeamLead,
        related_name="assigned_work",
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=150)
    client_name = models.CharField(max_length=120, blank=True)
    campaign_name = models.CharField(max_length=150)
    campaign_type = models.CharField(
        max_length=30,
        choices=CampaignType.choices,
        default=CampaignType.PAID_ADS,
    )
    channel = models.CharField(
        max_length=30,
        choices=Channel.choices,
        default=Channel.FACEBOOK,
    )
    responsibility = models.TextField()
    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default=Priority.MEDIUM,
    )
    status = models.CharField(
        max_length=30,
        choices=WorkStatus.choices,
        default=WorkStatus.NOT_STARTED,
    )
    progress = models.PositiveSmallIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    start_date = models.DateField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-due_date", "-created_at"]

    def __str__(self):
        return f"{self.title} - {self.team_lead.full_name}"
