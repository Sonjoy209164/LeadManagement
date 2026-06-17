from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Count


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


class Lead(models.Model):
    class Source(models.TextChoices):
        FORM = "form", "Form"
        WEBSITE = "website", "Website"
        CHAT = "chat", "Chat"
        SOCIAL_MEDIA = "social_media", "Social Media"
        EMAIL_CAMPAIGN = "email_campaign", "Email Campaign"
        EVENT = "event", "Event"
        REFERRAL = "referral", "Referral"
        PAID_ADS = "paid_ads", "Paid Ads"

    class Status(models.TextChoices):
        NEW = "new", "New"
        CONTACTED = "contacted", "Contacted"
        QUALIFIED = "qualified", "Qualified"
        CONVERTED = "converted", "Converted"
        LOST = "lost", "Lost"

    class Grade(models.TextChoices):
        HOT = "hot", "Hot"
        WARM = "warm", "Warm"
        COLD = "cold", "Cold"

    full_name = models.CharField(max_length=120)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    company_name = models.CharField(max_length=120, blank=True)
    industry = models.CharField(max_length=80, blank=True)
    annual_revenue = models.PositiveIntegerField(default=0)
    source = models.CharField(max_length=30, choices=Source.choices, default=Source.WEBSITE)
    assigned_to = models.ForeignKey(
        TeamLead,
        related_name="scored_leads",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    email_engagement = models.PositiveSmallIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    social_engagement = models.PositiveSmallIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    website_visits = models.PositiveSmallIntegerField(default=0)
    form_submissions = models.PositiveSmallIntegerField(default=0)
    lead_score = models.PositiveSmallIntegerField(default=0, editable=False)
    lead_grade = models.CharField(
        max_length=10,
        choices=Grade.choices,
        default=Grade.COLD,
        editable=False,
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-lead_score", "-updated_at"]

    def __str__(self):
        return f"{self.full_name} - {self.lead_score}"

    def save(self, *args, **kwargs):
        self.lead_score = self.calculate_score()
        self.lead_grade = self.calculate_grade(self.lead_score)
        if not self.assigned_to_id:
            self.assigned_to = self.auto_assign_team_lead()
        super().save(*args, **kwargs)

    def calculate_score(self):
        score = 0
        score += min(self.email_engagement, 100) * 0.25
        score += min(self.social_engagement, 100) * 0.20
        score += min(self.website_visits, 20) / 20 * 15
        score += min(self.form_submissions, 5) / 5 * 15
        score += self.revenue_score()
        score += self.industry_score()
        return min(round(score), 100)

    def revenue_score(self):
        if self.annual_revenue >= 1000000:
            return 15
        if self.annual_revenue >= 500000:
            return 12
        if self.annual_revenue >= 100000:
            return 8
        if self.annual_revenue > 0:
            return 4
        return 0

    def industry_score(self):
        high_fit = {"saas", "ecommerce", "real estate", "education", "finance", "retail"}
        return 10 if self.industry.strip().lower() in high_fit else 4 if self.industry else 0

    def auto_assign_team_lead(self):
        active_team_leads = TeamLead.objects.filter(status=TeamLead.Status.ACTIVE)
        if not active_team_leads.exists():
            return None

        specialization = self.target_specialization()
        if self.lead_grade == self.Grade.HOT and specialization:
            match = self.lowest_load_match(active_team_leads, specialization)
            if match:
                return match

        if specialization:
            match = self.lowest_load_match(active_team_leads, specialization)
            if match:
                return match

        return (
            active_team_leads.annotate(lead_count=Count("scored_leads"))
            .order_by("lead_count", "full_name")
            .first()
        )

    def target_specialization(self):
        source_map = {
            self.Source.FORM: "Lead Generation",
            self.Source.PAID_ADS: "Paid Ads",
            self.Source.SOCIAL_MEDIA: "Social Media",
            self.Source.WEBSITE: "SEO",
            self.Source.EMAIL_CAMPAIGN: "Email",
            self.Source.CHAT: "Lead Generation",
        }
        return source_map.get(self.source, "")

    def lowest_load_match(self, queryset, specialization):
        return (
            queryset.filter(specialization__icontains=specialization)
            .annotate(lead_count=Count("scored_leads"))
            .order_by("lead_count", "full_name")
            .first()
        )

    @staticmethod
    def calculate_grade(score):
        if score >= 75:
            return Lead.Grade.HOT
        if score >= 45:
            return Lead.Grade.WARM
        return Lead.Grade.COLD
