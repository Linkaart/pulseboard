from django.db import models

from apps.companies.models import Company
from apps.accounts.models import User


class MetricSnapshot(models.Model):
    """Agregat de metriques calculees pour une periode donnee."""

    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="metric_snapshots"
    )
    period_start = models.DateField()
    period_end = models.DateField()
    mrr = models.DecimalField(max_digits=12, decimal_places=2)
    churn_rate = models.FloatField()
    conversion_rate = models.FloatField()
    arpu = models.DecimalField(max_digits=10, decimal_places=2)
    new_customers = models.IntegerField()

    def __str__(self):
        return f"{self.company.name} {self.period_start} - {self.period_end}"


class SavedFilter(models.Model):
    """Filtre enregistre par un utilisateur pour retrouver une vue."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="saved_filters"
    )
    name = models.CharField(max_length=100)
    payload_json = models.JSONField()

    def __str__(self):
        return f"{self.name} ({self.user.username})"
