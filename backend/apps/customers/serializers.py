from rest_framework import serializers

from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            "id",
            "company",
            "name",
            "email",
            "phone",
            "status",
            "mrr",
            "owner",
            "created_at",
            "last_activity_at",
        ]
        read_only_fields = ["id", "created_at"]
