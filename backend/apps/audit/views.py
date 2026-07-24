from rest_framework import mixins, permissions, viewsets

from .models import ActivityLog
from .serializers import ActivityLogSerializer


class ActivityLogViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = ActivityLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ActivityLog.objects.filter(
            user__company_id=self.request.user.company_id
        )
