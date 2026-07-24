from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("apps.accounts.urls")),
    path("api/companies/", include("apps.companies.urls")),
    path("api/customers/", include("apps.customers.urls")),
    path("api/audit/", include("apps.audit.urls")),
    path("api/", include("apps.analytics.urls")),
    path("api/exports/", include("apps.exports.urls")),
]
