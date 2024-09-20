from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class ShiftListCreateView(generics.ListCreateAPIView):
    queryset = Shift.objects.all().order_by('-id')
    serializer_class = ShiftSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    

class ShiftRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializer

    def patch(self, request, *args, **kwargs):
        """
        Partially update a Shift instance, specifically updating the status field.
        """
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Return the updated instance
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        """
        Save the updated status field in the Shift instance.
        """
        # Check if 'status' is in the request data to update it
        if 'status' in serializer.validated_data:
            serializer.save(status=serializer.validated_data['status'])
        else:
            serializer.save()

class ShiftDetailsListCreateView(generics.ListCreateAPIView):
    queryset=ShiftDetails.objects.all()
    serializer_class=ShiftDetailsSerializer

class ShiftDetailsRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset=ShiftDetails.objects.all()
    serializer_class=ShiftDetailsSerializer

class ShiftDetailsByShiftIDView(APIView):
    def get(self, request, pk, format=None):
        # Filter ShiftDetails by the provided shift_id (pk)
        shift_details = ShiftDetails.objects.filter(shift_id=pk)
        if shift_details.exists():
            serializer = ShiftDetailsSerializer(shift_details, many=True)
            return Response(serializer.data)
        return Response({'detail': 'No shift details found for this shift ID.'}, status=status.HTTP_404_NOT_FOUND)
    

class ShiftBaggingOffListCreateView(generics.ListCreateAPIView):
    queryset = ShiftBaggingOff.objects.all().order_by('-id')
    serializer_class = ShiftBaggingOffSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class ShiftBaggingOffRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ShiftBaggingOff.objects.all()
    serializer_class = ShiftBaggingOffSerializer

    def patch(self, request, *args, **kwargs):
        """
        Partially update a ShiftBaggingOff instance, specifically updating the status field.
        """
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Return the updated instance
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        """
        Save the updated status field in the ShiftBaggingOff instance.
        """
        # Check if 'status' is in the request data to update it
        if 'status' in serializer.validated_data:
            serializer.save(status=serializer.validated_data['status'])
        else:
            serializer.save()

class ShiftDetailsBaggingOffListCreateView(generics.ListCreateAPIView):
    queryset = ShiftDetailsBaggingOff.objects.all()
    serializer_class = ShiftDetailsBaggingOffSerializer

class ShiftDetailsBaggingOffRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ShiftDetailsBaggingOff.objects.all()
    serializer_class = ShiftDetailsBaggingOffSerializer

class ShiftDetailsBaggingOffByShiftIDView(APIView):
    def get(self, request, pk, format=None):
        shift_details = ShiftDetailsBaggingOff.objects.filter(shiftbaggingoff_id=pk)
        if shift_details.exists():
            serializer = ShiftDetailsBaggingOffSerializer(shift_details, many=True)
            return Response(serializer.data)
        return Response({'detail': 'No shift details found for this bagging off shift ID.'}, status=status.HTTP_404_NOT_FOUND)