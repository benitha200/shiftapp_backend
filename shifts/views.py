from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


# Create your views here.

class ShiftListCreateView(generics.ListCreateAPIView):
    queryset = Shift.objects.all().order_by('-id')
    serializer_class = ShiftSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class ShiftRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Shift.objects.all()
    serializer_class=ShiftSerializer

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