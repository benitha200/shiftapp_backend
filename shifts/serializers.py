from rest_framework import serializers
from .models import Shift, ShiftDetails

class ShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shift
        fields = ['id', 'shift_no', 'activity', 'date', 'created_at']

class ShiftDetailsSerializer(serializers.ModelSerializer):
    shift_id = serializers.IntegerField(write_only=True)
    shift = ShiftSerializer(read_only=True)

    class Meta:
        model = ShiftDetails
        fields = ['id', 'shift_id', 'shift', 'supplier', 'grade', 'total_kgs', 'total_bags', 'batchno_grn', 'cell', 'entry_type']

    def create(self, validated_data):
        shift_id = validated_data.pop('shift_id')
        shift = Shift.objects.get(id=shift_id)
        return ShiftDetails.objects.create(shift=shift, **validated_data)
