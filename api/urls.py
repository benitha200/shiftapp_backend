from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from accounts.views import UserRegistrationView, CustomTokenObtainPairView
from shifts.views import (
    ShiftListCreateView,
    ShiftRetrieveUpdateDestroyView,
    ShiftDetailsListCreateView,
    ShiftDetailsRetrieveUpdateDestroyView,
    ShiftDetailsByShiftIDView,
    ShiftBaggingOffListCreateView,
    ShiftBaggingOffRetrieveUpdateDestroyView,
    ShiftDetailsBaggingOffListCreateView,
    ShiftDetailsBaggingOffRetrieveUpdateDestroyView,
    ShiftDetailsBaggingOffByShiftIDView,
)

from reports.views import (
    ShiftSummaryReportView,
    ShiftDetailsReportView,
    AllShiftsReportView,
    CombinedShiftsReportView
)

urlpatterns = [
    path('shifts/',ShiftListCreateView.as_view(),name="shift-list-create"),
    path('shifts/<int:pk>',ShiftRetrieveUpdateDestroyView.as_view(),name="shift-retrieve-update-destroy-view"),
    path('shiftdetails/',ShiftDetailsListCreateView.as_view(),name="shift-details-list-create"),
    path('shiftdetails/<int:pk>',ShiftDetailsRetrieveUpdateDestroyView.as_view(),name="shift-details-retrieve-update-destroy-view"),
    path('shiftdetail/<int:pk>/', ShiftDetailsByShiftIDView.as_view(), name='shiftdetails-by-shift-id'),
    path('baggingoff-shifts/', ShiftBaggingOffListCreateView.as_view(), name='baggingoff-shift-list-create'),
    path('baggingoff-shifts/<int:pk>/', ShiftBaggingOffRetrieveUpdateDestroyView.as_view(), name='baggingoff-shift-detail'),
    path('baggingoff-shift-details/', ShiftDetailsBaggingOffListCreateView.as_view(), name='baggingoff-shift-details-list-create'),
    path('baggingoff-shift-details/<int:pk>/', ShiftDetailsBaggingOffRetrieveUpdateDestroyView.as_view(), name='baggingoff-shift-details-detail'),
    path('baggingoff-shifts/<int:pk>/details/', ShiftDetailsBaggingOffByShiftIDView.as_view(), name='baggingoff-shift-details-by-id'),
    path('shift-summary-report/',ShiftSummaryReportView.as_view(),name='shift-summary-report'),
    path('shift-details-report/',ShiftDetailsReportView.as_view(),name='shift-details-report'),
    path('all-shifts-report/',AllShiftsReportView.as_view(),name='shift-details-report'),
    path('combined-shifts-report/', CombinedShiftsReportView.as_view(), name='combined-shifts-report'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
