from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Utilisateur personnalise, rattache a une entreprise et une equipe."""

    company = models.ForeignKey(
        "companies.Company", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="users"
    )
    team = models.ForeignKey(
        "companies.Team", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="members"
    )

    def __str__(self):
        return self.username
