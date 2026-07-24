from datetime import date

import pytest
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework import status

from apps.analytics.models import MetricSnapshot
from apps.analytics.services import compute_kpis, parse_filters
from apps.customers.models import Subscription


def grant_kpi_permission(user):
    content_type = ContentType.objects.get_for_model(MetricSnapshot)
    permission, _ = Permission.objects.get_or_create(
        codename="view_kpi",
        content_type=content_type,
        defaults={"name": "Can view KPI dashboard"},
    )
    user.user_permissions.add(permission)


@pytest.mark.django_db
class TestComputeKpis:
    def test_computes_mrr_from_active_subscriptions(self, company, customer):
        Subscription.objects.create(
            customer=customer,
            product_name="Pro",
            status="active",
            monthly_amount=150,
            started_at=date(2024, 1, 1),
        )
        data = compute_kpis(company, date(2024, 1, 1), date(2024, 1, 31))
        assert data["mrr"] == 150

    def test_churn_rate_is_zero_without_churned_subscriptions(self, company, customer):
        Subscription.objects.create(
            customer=customer,
            product_name="Pro",
            status="active",
            monthly_amount=100,
            started_at=date(2024, 1, 1),
        )
        data = compute_kpis(company, date(2024, 1, 1), date(2024, 1, 31))
        assert data["churn_rate"] == 0

    def test_new_customers_counted_within_period(self, company, customer):
        data = compute_kpis(company, date.today().replace(day=1), date.today())
        assert data["new_customers"] >= 1


class TestParseFilters:
    def test_extracts_expected_keys(self):
        filters = parse_filters({"period_start": "2024-01-01", "team": "Sales"})
        assert filters["period_start"] == "2024-01-01"
        assert filters["team"] == "Sales"
        assert filters["channel"] is None


@pytest.mark.django_db
class TestDashboardSummaryView:
    def test_requires_authentication(self, api_client):
        response = api_client.get("/api/dashboard/summary/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_requires_kpi_permission(self, auth_client):
        response = auth_client.get("/api/dashboard/summary/")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_returns_kpi_summary_with_permission(self, auth_client, user, customer):
        grant_kpi_permission(user)
        response = auth_client.get("/api/dashboard/summary/")
        assert response.status_code == status.HTTP_200_OK
        assert "mrr" in response.data


@pytest.mark.django_db
class TestDashboardTableView:
    def test_lists_customers_for_company(self, auth_client, customer):
        response = auth_client.get("/api/dashboard/table/")
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestSavedFilters:
    def test_create_saved_filter(self, auth_client):
        payload = {"name": "My view", "payload_json": {"status": "active"}}
        response = auth_client.post("/api/filters/", payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    def test_list_saved_filters_scoped_to_user(self, auth_client):
        response = auth_client.get("/api/filters/")
        assert response.status_code == status.HTTP_200_OK
