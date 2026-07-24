from django.urls import path

from .views import (
    DashboardSummaryView, DashboardChartsView, DashboardTableView,
    SavedFilterListCreateView,
)

urlpatterns = [
    path("dashboard/summary/", DashboardSummaryView.as_view(), name="dashboard-summary"),
    path("dashboard/charts/", DashboardChartsView.as_view(), name="dashboard-charts"),
    path("dashboard/table/", DashboardTableView.as_view(), name="dashboard-table"),
    path("filters/", SavedFilterListCreateView.as_view(), name="saved-filters"),
]
