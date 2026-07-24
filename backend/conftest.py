import pytest
from datetime import date
from rest_framework.test import APIClient

from apps.companies.models import Company, Team
from apps.customers.models import Customer, Subscription, Invoice

from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def company(db):
    return Company.objects.create(name="Acme Corp")


@pytest.fixture
def team(db, company):
    return Team.objects.create(company=company, name="Sales")


@pytest.fixture
def user(db, company, team):
    return User.objects.create_user(
        username="jdoe",
        email="jdoe@example.com",
        password="StrongPass123",
        first_name="John",
        last_name="Doe",
        company=company,
        team=team,
    )


@pytest.fixture
def other_company(db):
    return Company.objects.create(name="Other Corp")


@pytest.fixture
def other_user(db, other_company):
    return User.objects.create_user(
        username="other",
        email="other@example.com",
        password="StrongPass123",
        company=other_company,
    )


@pytest.fixture
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def customer(db, company, user):
    return Customer.objects.create(
        company=company,
        name="Client A",
        segment="SMB",
        acquisition_channel="Referral",
        email="clienta@example.com",
        status="active",
        mrr=100,
        owner=user,
    )


@pytest.fixture
def subscription(db, customer):
    return Subscription.objects.create(
        customer=customer,
        product_name="Pro Plan",
        status="active",
        monthly_amount=100,
        started_at=date(2024, 1, 1),
    )


@pytest.fixture
def invoice(db, subscription):
    return Invoice.objects.create(
        subscription=subscription,
        amount=100,
        status="paid",
        billed_at=date(2024, 1, 1),
        paid_at=date(2024, 1, 2),
    )
