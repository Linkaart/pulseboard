from rest_framework import serializers

from .models import ActivityLog


class ActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityLog
        fields = ["id", "user", "action", "entity_type", "entity_id", "created_at"]
        read_only_fields = fields
