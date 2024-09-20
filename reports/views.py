from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from shifts.models import Shift, ShiftDetails,ShiftBaggingOff,ShiftDetailsBaggingOff
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
          # 'input_output_ratio': input_output_ratio,
          'production_loss': production_loss,
          'production_gain': production_gain,
      })

    return Response(report_data, status=status.HTTP_200_OK)
  

class ShiftDetailsReportView(APIView):
    def generate_report(self, start_date, end_date):
        shifts = Shift.objects.filter(date__range=[start_date, end_date]).order_by('-id')
        
        if not shifts.exists():
            return None

        report_data = []
        for shift in shifts:
            shift_details = ShiftDetails.objects.filter(shift=shift)
            
            for detail in shift_details:
                report_data.append({
                    'shift_no': shift.shift_no,
                    'supplier': shift.supplier,
                    'date': shift.date,
                    'activity': shift.activity,
                    'status': detail.entry_type,
                    'grade': detail.grade,
                    'total_bags': detail.total_bags,
                    'total_kgs': detail.total_kgs,
                    'batchno_grn': detail.batchno_grn,
                    'cell': detail.cell,
                })
        
        return report_data

    def post(self, request, format=None):
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        
        if not start_date or not end_date:
            return Response({'error':'start_date and end_date are required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        report_data = self.generate_report(start_date, end_date)
        
        if report_data is None:
            return Response({'detail': 'No shifts found within the specified date range.'}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(report_data, status=status.HTTP_200_OK)

class AllShiftsReportView(APIView):
    def generate_report(self, start_date, end_date):
        shifts = Shift.objects.filter(date__range=[start_date, end_date]).order_by('-id')
        
        if not shifts.exists():
            return None

        report_data = []
        for shift in shifts:
            shift_details = ShiftDetails.objects.filter(shift=shift)
            
            for detail in shift_details:
                report_data.append({
                    'shift_no': shift.shift_no,
                    'activity': shift.activity,
                    'date': shift.date,
                    'supplier': shift.supplier,
                    'shift_type': shift.shift_type,
                    'coffee_type': shift.coffee_type,
                    'output_batchno': shift.output_batchno,
                    'completion_status': shift.status,
                    'grade': detail.grade,
                    'total_kgs': detail.total_kgs,
                    'total_bags': detail.total_bags,
                    'batchno_grn': detail.batchno_grn,
                    'cell': detail.cell,
                    'entry_type': detail.entry_type,
                    'created_by': shift.created_by.email,
                })
        
        return report_data

    def post(self, request, format=None):
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        
        if not start_date or not end_date:
            return Response({'error':'start_date and end_date are required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        report_data = self.generate_report(start_date, end_date)
        
        if report_data is None:
            return Response({'detail': 'No shifts found within the specified date range.'}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(report_data, status=status.HTTP_200_OK)
    

class CombinedShiftsReportView(APIView):
    def generate_report(self, start_date, end_date):
        # Query regular shifts
        shifts = Shift.objects.filter(date__range=[start_date, end_date]).order_by('-id')
        
        # Query bagging off shifts
        bagging_off_shifts = ShiftBaggingOff.objects.filter(date__range=[start_date, end_date]).order_by('-id')
        
        if not shifts.exists() and not bagging_off_shifts.exists():
            return None

        report_data = []

        # Process regular shifts
        for shift in shifts:
            shift_details = ShiftDetails.objects.filter(shift=shift)
            
            for detail in shift_details:
                report_data.append({
                    'shift_type': 'Regular',
                    'shift_no': shift.shift_no,
                    'activity': shift.activity,
                    'date': shift.date,
                    'supplier': shift.supplier,
                    'coffee_type': shift.coffee_type,
                    'output_batchno': shift.output_batchno,
                    'completion_status': shift.status,
                    'grade': detail.grade,
                    'total_kgs': detail.total_kgs,
                    'total_bags': detail.total_bags,
                    'batchno_grn': detail.batchno_grn,
                    'cell': detail.cell,
                    'entry_type': detail.entry_type,
                    'created_by': shift.created_by.email,
                })

        # Process bagging off shifts
        for bagging_shift in bagging_off_shifts:
            bagging_shift_details = ShiftDetailsBaggingOff.objects.filter(shiftbaggingoff=bagging_shift)
            
            for detail in bagging_shift_details:
                report_data.append({
                    'shift_type': 'Bagging Off',
                    'shift_no': bagging_shift.shift_no_bagging_off,
                    'activity': bagging_shift.activity,
                    'date': bagging_shift.date,
                    'completion_status': bagging_shift.status,
                    'grade': detail.grade,
                    'total_kgs': detail.total_kgs,
                    'total_bags': detail.total_bags,
                    'batchno_grn': detail.batchno_grn,
                    'cell': detail.cell,
                    'entry_type': detail.entry_type,
                    'created_by': bagging_shift.created_by.email,
                    'created_at': bagging_shift.created_at,
                    'lot_no': detail.lot_no,  # Added lot_no for bagging off shifts
                    'supplier': detail.supplier,  # Added supplier for bagging off shifts
                    'balance': detail.balance,  # Added balance for bagging off shifts
                    'loss': detail.loss,  # Added loss for bagging off shifts
                    'stock_card': detail.stock_card,  # Added stock_card for bagging off shifts
                    'parch_grade': detail.parch_grade,  # Added parch_grade for bagging off shifts
                    'year': detail.year,  # Added year for bagging off shifts
                })
        
        return report_data

    def post(self, request, format=None):
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        
        if not start_date or not end_date:
            return Response({'error':'start_date and end_date are required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        report_data = self.generate_report(start_date, end_date)
        
        if report_data is None:
            return Response({'detail': 'No shifts found within the specified date range.'}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(report_data, status=status.HTTP_200_OK)