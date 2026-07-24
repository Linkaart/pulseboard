from datetime import date, timedelta

from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.customers.models import Customer
from .models import SavedFilter
from .serializers import (
    KPISummarySerializer, CustomerTableSerializer, SavedFilterSerializer,
)
from .services import compute_kpis, parse_filters


class HasKPIPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm("analytics.view_kpi")


class DashboardSummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated, HasKPIPermission]

    def get(self, request):
        company = request.user.company
        filters = parse_filters(request.query_params)
        period_end = date.today()
        period_start = period_end - timedelta(days=30)
        data = compute_kpis(company, period_start, period_end)
        return Response(KPISummarySerializer(data).data)


class DashboardChartsView(APIView):
    permission_classes = [permissions.IsAuthenticated, HasKPIPermission]

    def get(self, request):
        company = request.user.company
        snapshots = company.metric_snapshots.order_by("period_start")
        series = [
            {
                "period": s.period_start.isoformat(),
                "mrr": str(s.mrr),
                "new_customers": s.new_customers,
                "churn_rate": s.churn_rate,
            }
            for s in snapshots
        ]
        return Response(series)


class DashboardTableView(generics.ListAPIView):
    serializer_class = CustomerTableSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Customer.objects.filter(company=self.request.user.company)


class SavedFilterListCreateView(generics.ListCreateAPIView):
    serializer_class = SavedFilterSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SavedFilter.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
