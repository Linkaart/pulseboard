import csv

from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from apps.customers.models import Customer
from apps.audit.models import ActivityLog


class ExportCustomersCSVView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="customers.csv"'
        writer = csv.writer(response)
        writer.writerow(["Nom", "Segment", "Canal", "Statut abonnement"])

        customers = Customer.objects.filter(company=request.user.company)
        for c in customers:
            sub = c.subscriptions.first()
            writer.writerow([
                c.name, c.segment, c.acquisition_channel,
                sub.status if sub else "",
            ])

        ActivityLog.objects.create(
            user=request.user, action="export_csv", entity_type="Customer"
        )
        return response
