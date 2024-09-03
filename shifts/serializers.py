from rest_framework import serializers
from .models import Shift, ShiftDetails
from accounts.serializers import UserSerializer


class ShiftSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Shift
        fields = ['id', 'shift_no', 'activity', 'date', 'shift_type', 'supplier', 'coffee_type', 'output_batchno', 'location_of_batch', 'created_by', 'created_at','status']
        read_only_fields = ['created_by', 'created_at']

    def validate_shift_no(self, value):
        if Shift.objects.filter(shift_no=value).exists():
            raise serializers.ValidationError(_("Shift no already exists"))
        return value


class ShiftDetailsSerializer(serializers.ModelSerializer):
    shift_id = serializers.IntegerField(write_only=True)
    shift = ShiftSerializer(read_only=True)

    class Meta:
        model = ShiftDetails
        fields = ['id', 'shift_id', 'shift', 'grade', 'total_kgs', 'total_bags', 'batchno_grn', 'cell', 'entry_type']

    def create(self, validated_data):
        shift_id = validated_data.pop('shift_id')
        shift = Shift.objects.get(id=shift_id)
        return ShiftDetails.objects.create(shift=shift, **validated_data)
