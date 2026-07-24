from django.db import models

from apps.companies.models import Company


class Customer(models.Model):
    """Client final d'une entreprise utilisant PulseBoard."""

    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="customers"
    )
    name = models.CharField(max_length=255)
    segment = models.CharField(max_length=100, blank=True)
    acquisition_channel = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    """Abonnement souscrit par un client."""

    STATUS_CHOICES = [
        ("trial", "Essai"),
        ("active", "Actif"),
        ("churned", "Resilie"),
    ]

    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="subscriptions"
    )
    product_name = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="trial")
    monthly_amount = models.DecimalField(max_digits=10, decimal_places=2)
    started_at = models.DateField()
    ended_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.product_name} - {self.customer.name}"


class Invoice(models.Model):
    """Facture liee a un abonnement."""

    STATUS_CHOICES = [
        ("pending", "En attente"),
        ("paid", "Payee"),
        ("failed", "Echouee"),
    ]

    subscription = models.ForeignKey(
        Subscription, on_delete=models.CASCADE, related_name="invoices"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    billed_at = models.DateField()
    paid_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Facture #{self.id} - {self.subscription}"
