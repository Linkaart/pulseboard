import pytest
from rest_framework import status

from apps.audit.models import ActivityLog


@pytest.mark.django_db
class TestActivityLogViewSet:
    def test_requires_authentication(self, api_client):
        response = api_client.get("/api/audit/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_lists_logs_for_own_company_only(self, auth_client, user, other_user):
        ActivityLog.objects.create(user=user, action="login", entity_type="session")
        ActivityLog.objects.create(user=other_user, action="login", entity_type="session")
        response = auth_client.get("/api/audit/")
        assert response.status_code == status.HTTP_200_OK
        results = response.data["results"] if "results" in response.data else response.data
        assert len(results) == 1

    def test_logs_ordered_by_most_recent_first(self, auth_client, user):
        first = ActivityLog.objects.create(user=user, action="create", entity_type="customer")
        second = ActivityLog.objects.create(user=user, action="update", entity_type="customer")
        response = auth_client.get("/api/audit/")
        results = response.data["results"] if "results" in response.data else response.data
        assert results[0]["id"] == second.id
        assert results[1]["id"] == first.id
