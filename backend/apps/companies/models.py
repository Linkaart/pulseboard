from django.db import models


class Company(models.Model):
    """Entreprise cliente de la plateforme SaaS."""

    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Team(models.Model):
    """Equipe rattachee a une entreprise."""

    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="teams"
    )
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} ({self.company.name})"
