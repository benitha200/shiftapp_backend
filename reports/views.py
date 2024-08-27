# # working shift summary report without input vs output ratio and production loses and gains

# from django.shortcuts import render
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from shifts.models import Shift, ShiftDetails
# from shifts.serializers import ShiftSerializer
# from django.db.models import Sum

# class ShiftSummaryReportView(APIView):
#     def post(self, request, format=None):
#         start_date = request.data.get('start_date')
#         end_date = request.data.get('end_date')

#         if not start_date or not end_date:
#             return Response({'error': 'start_date and end_date are required.'}, status=status.HTTP_400_BAD_REQUEST)

#         # Retrieve all shifts within the specified date range
#         shifts = Shift.objects.filter(date__range=[start_date, end_date])

#         if not shifts.exists():
#             return Response({'detail': 'No shifts found within the specified date range.'}, status=status.HTTP_404_NOT_FOUND)

#         report_data = []
#         for shift in shifts:
#             shift_details = ShiftDetails.objects.filter(shift=shift)

#             total_input_kgs = shift_details.filter(entry_type='Input').aggregate(Sum('total_kgs'))['total_kgs__sum'] or 0
#             total_input_bags = shift_details.filter(entry_type='Input').aggregate(Sum('total_bags'))['total_bags__sum'] or 0
#             total_output_kgs = shift_details.filter(entry_type='Output').aggregate(Sum('total_kgs'))['total_kgs__sum'] or 0
#             total_balance_kgs = shift_details.filter(entry_type='Balance').aggregate(Sum('total_kgs'))['total_kgs__sum'] or 0

#             report_data.append({
#                 'shift_no': shift.shift_no,
#                 'date': shift.date,
#                 'activity': shift.activity,
#                 'total_input_kgs': total_input_kgs,
#                 'total_input_bags': total_input_bags,
#                 'total_output_kgs': total_output_kgs,
#                 'total_balance_kgs': total_balance_kgs,
#             })

#         return Response(report_data, status=status.HTTP_200_OK)


from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from shifts.models import Shift, ShiftDetails
from shifts.serializers import ShiftSerializer
from django.db.models import Sum

class ShiftSummaryReportView(APIView):
  def post(self, request, format=None):
    start_date = request.data.get('start_date')
    end_date = request.data.get('end_date')

    if not start_date or not end_date:
      return Response({'error':'start_date and end_date are required.'}, status=status.HTTP_400_BAD_REQUEST)


    # Retrieve all shifts within the specified date range
    shifts = Shift.objects.filter(date__range=[start_date, end_date]).order_by('-id')

    if not shifts.exists():
      return Response({'detail': 'No shifts found within the specified date range.'}, status=status.HTTP_404_NOT_FOUND)

    report_data = []
    for shift in shifts:
      shift_details = ShiftDetails.objects.filter(shift=shift)

      total_input_kgs = shift_details.filter(entry_type='Input').aggregate(Sum('total_kgs'))['total_kgs__sum'] or 0
      total_output_kgs = shift_details.filter(entry_type='Output').aggregate(Sum('total_kgs'))['total_kgs__sum'] or 0

      # Calculate input vs output ratio (handle division by zero)
      input_output_ratio = total_input_kgs / (total_output_kgs or 1)  # Avoid division by zero

      # Calculate production losses (assuming higher input is a loss)
      production_loss = max(0, total_input_kgs - total_output_kgs)

      # Calculate production gains (assuming higher output is a gain)
      production_gain = max(0, total_output_kgs - total_input_kgs)

      report_data.append({
          'shift_no': shift.shift_no,
          'date': shift.date,
          'activity': shift.activity,
          'total_input_kgs': total_input_kgs,
          'total_output_kgs': total_output_kgs,
          'input_output_ratio': input_output_ratio,
          'production_loss': production_loss,
          'production_gain': production_gain,
      })

    return Response(report_data, status=status.HTTP_200_OK)