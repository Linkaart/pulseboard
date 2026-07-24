from django.urls import path

from .views import ExportCustomersCSVView

app_name = "exports"

urlpatterns = [
    path("customers.csv/", ExportCustomersCSVView.as_view(), name="export_customers_csv"),
]
