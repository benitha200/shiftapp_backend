from django.urls import path
from shifts.views import (
    ShiftListCreateView,
    ShiftRetrieveUpdateDestroyView,
    ShiftDetailsListCreateView,
    ShiftDetailsRetrieveUpdateDestroyView,
    ShiftDetailsByShiftIDView
)

from reports.views import (
    ShiftSummaryReportView
)

urlpatterns = [
    path('shifts/',ShiftListCreateView.as_view(),name="shift-list-create"),
    path('shifts/<int:pk>',ShiftRetrieveUpdateDestroyView.as_view(),name="shift-retrieve-update-destroy-view"),
    path('shiftdetails/',ShiftDetailsListCreateView.as_view(),name="shift-details-list-create"),
    path('shiftdetails/<int:pk>',ShiftDetailsRetrieveUpdateDestroyView.as_view(),name="shift-details-retrieve-update-destroy-view"),
    path('shiftdetail/<int:pk>/', ShiftDetailsByShiftIDView.as_view(), name='shiftdetails-by-shift-id'),
    path('shift-summary-report/',ShiftSummaryReportView.as_view(),name='shift-summary-report'),
]
