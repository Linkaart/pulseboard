from rest_framework import serializers

from apps.customers.models import Customer
from .models import MetricSnapshot, SavedFilter


class MetricSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetricSnapshot
        fields = [
            "period_start", "period_end", "mrr", "churn_rate",
            "conversion_rate", "arpu", "new_customers",
        ]


class KPISummarySerializer(serializers.Serializer):
    mrr = serializers.DecimalField(max_digits=12, decimal_places=2)
    churn_rate = serializers.FloatField()
    conversion_rate = serializers.FloatField()
    arpu = serializers.DecimalField(max_digits=10, decimal_places=2)
    new_customers = serializers.IntegerField()


class CustomerTableSerializer(serializers.ModelSerializer):
    subscription_status = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = [
            "id", "name", "segment", "acquisition_channel",
            "created_at", "subscription_status",
        ]

    def get_subscription_status(self, obj):
        sub = obj.subscriptions.first()
        return sub.status if sub else None


class SavedFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedFilter
        fields = ["id", "name", "payload_json"]
