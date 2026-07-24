"""Fonctions de calcul des KPI a partir des donnees clients/abonnements."""
from datetime import date

from apps.customers.models import Customer, Subscription


def compute_kpis(company, period_start: date, period_end: date) -> dict:
    """Calcule les KPI principaux pour une entreprise sur une periode donnee."""
    customers = Customer.objects.filter(company=company)
    subscriptions = Subscription.objects.filter(customer__company=company)

    active_subs = subscriptions.filter(status="active")
    churned_subs = subscriptions.filter(
        status="churned", ended_at__range=(period_start, period_end)
    )
    new_customers = customers.filter(
        created_at__date__range=(period_start, period_end)
    ).count()

    mrr = sum(sub.monthly_amount for sub in active_subs)
    total_subs = subscriptions.count() or 1
    churn_rate = churned_subs.count() / total_subs * 100
    arpu = mrr / active_subs.count() if active_subs.count() else 0
    conversion_rate = (
        active_subs.count() / customers.count() * 100 if customers.count() else 0
    )

    return {
        "mrr": mrr,
        "churn_rate": round(churn_rate, 2),
        "conversion_rate": round(conversion_rate, 2),
        "arpu": round(arpu, 2),
        "new_customers": new_customers,
    }


def parse_filters(query_params) -> dict:
    """Extrait et normalise les filtres depuis les query params de la requete."""
    return {
        "period_start": query_params.get("period_start"),
        "period_end": query_params.get("period_end"),
        "team": query_params.get("team"),
        "channel": query_params.get("channel"),
        "product": query_params.get("product"),
    }
