from rest_framework import serializers

from .models import AssignedWork, TeamLead


class TeamLeadSerializer(serializers.ModelSerializer):
    assigned_work_count = serializers.SerializerMethodField()

    class Meta:
        model = TeamLead
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")

    def get_assigned_work_count(self, obj):
        return obj.assigned_work.count()


class AssignedWorkSerializer(serializers.ModelSerializer):
    team_lead_name = serializers.CharField(source="team_lead.full_name", read_only=True)

    class Meta:
        model = AssignedWork
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")

    def validate(self, attrs):
        start_date = attrs.get("start_date", getattr(self.instance, "start_date", None))
        due_date = attrs.get("due_date", getattr(self.instance, "due_date", None))

        if start_date and due_date and due_date < start_date:
            raise serializers.ValidationError("Due date cannot be earlier than start date.")

        progress = attrs.get("progress", getattr(self.instance, "progress", 0))
        if progress < 0 or progress > 100:
            raise serializers.ValidationError("Progress must be between 0 and 100.")

        status = attrs.get("status", getattr(self.instance, "status", "not_started"))
        if status == "completed" and progress != 100:
            attrs["progress"] = 100

        if progress == 100 and status not in ("completed", "cancelled"):
            attrs["status"] = "completed"

        return attrs
