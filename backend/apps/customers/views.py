from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets

from .models import Customer
from .serializers import CustomerSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["status", "owner"]
    search_fields = ["name", "email"]
    ordering_fields = ["created_at", "mrr", "last_activity_at"]

    def get_queryset(self):
        return Customer.objects.filter(company_id=self.request.user.company_id)

    def perform_create(self, serializer):
        serializer.save(company_id=self.request.user.company_id)
