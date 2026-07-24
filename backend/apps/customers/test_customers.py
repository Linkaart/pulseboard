import pytest
from rest_framework import status

from apps.customers.models import Customer


@pytest.mark.django_db
class TestCustomerList:
    def test_requires_authentication(self, api_client):
        response = api_client.get("/api/customers/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_lists_only_own_company_customers(self, auth_client, customer, other_company):
        Customer.objects.create(company=other_company, name="Other Client")
        response = auth_client.get("/api/customers/")
        assert response.status_code == status.HTTP_200_OK
        names = [c["name"] for c in response.data["results"]] if "results" in response.data else [c["name"] for c in response.data]
        assert "Client A" in names
        assert "Other Client" not in names

    def test_filter_by_status(self, auth_client, customer, company):
        Customer.objects.create(company=company, name="Inactive Client", status="inactive")
        response = auth_client.get("/api/customers/?status=active")
        assert response.status_code == status.HTTP_200_OK

    def test_search_by_name(self, auth_client, customer):
        response = auth_client.get("/api/customers/?search=Client A")
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestCustomerCreate:
    def test_create_customer_sets_company_automatically(self, auth_client, company):
        payload = {"name": "New Client", "segment": "Enterprise", "status": "active"}
        response = auth_client.post("/api/customers/", payload)
        assert response.status_code == status.HTTP_201_CREATED
        created = Customer.objects.get(name="New Client")
        assert created.company_id == company.id


@pytest.mark.django_db
class TestCustomerDetail:
    def test_retrieve_customer(self, auth_client, customer):
        response = auth_client.get(f"/api/customers/{customer.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == customer.name

    def test_update_customer(self, auth_client, customer):
        response = auth_client.patch(f"/api/customers/{customer.id}/", {"name": "Renamed"})
        assert response.status_code == status.HTTP_200_OK
        customer.refresh_from_db()
        assert customer.name == "Renamed"

    def test_delete_customer(self, auth_client, customer):
        response = auth_client.delete(f"/api/customers/{customer.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Customer.objects.filter(id=customer.id).exists()

    def test_cannot_access_other_company_customer(self, auth_client, other_company):
        other_customer = Customer.objects.create(company=other_company, name="Foreign")
        response = auth_client.get(f"/api/customers/{other_customer.id}/")
        assert response.status_code == status.HTTP_404_NOT_FOUND
