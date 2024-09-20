# from rest_framework import serializers
# from .models import Shift, ShiftDetails
# from accounts.serializers import UserSerializer


# class ShiftSerializer(serializers.ModelSerializer):
#     created_by = UserSerializer(read_only=True)

#     class Meta:
#         model = Shift
#         fields = ['id', 'shift_no', 'activity', 'date', 'shift_type', 'supplier', 'coffee_type', 'output_batchno', 'location_of_batch', 'created_by', 'created_at','status']
#         read_only_fields = ['created_by', 'created_at']

#     def validate_shift_no(self, value):
#         if Shift.objects.filter(shift_no=value).exists():
#             raise serializers.ValidationError(_("Shift no already exists"))
#         return value


# class ShiftDetailsSerializer(serializers.ModelSerializer):
#     shift_id = serializers.IntegerField(write_only=True)
#     shift = ShiftSerializer(read_only=True)

#     class Meta:
#         model = ShiftDetails
#         fields = ['id', 'shift_id', 'shift', 'grade', 'total_kgs', 'total_bags', 'batchno_grn', 'cell', 'entry_type']

#     def create(self, validated_data):
#         shift_id = validated_data.pop('shift_id')
#         shift = Shift.objects.get(id=shift_id)
#         return ShiftDetails.objects.create(shift=shift, **validated_data)

from rest_framework import serializers
from .models import Shift, ShiftDetails, ShiftBaggingOff, ShiftDetailsBaggingOff
from accounts.serializers import UserSerializer


class ShiftSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Shift
        fields = ['id', 'shift_no', 'activity', 'date', 'shift_type', 'supplier', 'coffee_type', 'output_batchno', 'location_of_batch', 'created_by', 'created_at', 'status']
        read_only_fields = ['created_by', 'created_at']

    def validate_shift_no(self, value):
        if Shift.objects.filter(shift_no=value).exists():
            raise serializers.ValidationError("Shift no already exists")
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


class ShiftBaggingOffSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = ShiftBaggingOff
        fields = ['id', 'shift_no_bagging_off', 'activity', 'date', 'status', 'created_by', 'created_at']
        read_only_fields = ['shift_no_bagging_off', 'created_by', 'created_at']

    # def create(self, validated_data):
    #     user = self.context['request'].user
    #     shift = ShiftBaggingOff.objects.create(created_by=user, **validated_data)
    #     return shift



class ShiftDetailsBaggingOffSerializer(serializers.ModelSerializer):
    shiftbaggingoff_id = serializers.IntegerField(write_only=True)
    shiftbaggingoff = ShiftBaggingOffSerializer(read_only=True)
    
    # Make fields optional
    stock_card = serializers.CharField(required=False, allow_blank=True)
    lot_no = serializers.CharField(required=False, allow_blank=True)
    year = serializers.IntegerField(required=False, default=2024)
    batchno_grn = serializers.CharField(required=False, default="000")

    class Meta:
        model = ShiftDetailsBaggingOff
        fields = ['id', 'shiftbaggingoff_id', 'shiftbaggingoff', 'grade', 'total_kgs', 'total_bags', 'balance', 'loss', 'supplier', 'cell', 'stock_card', 'lot_no', 'batchno_grn', 'parch_grade', 'year', 'entry_type']

    def create(self, validated_data):
        shiftbaggingoff_id = validated_data.pop('shiftbaggingoff_id')
        shiftbaggingoff = ShiftBaggingOff.objects.get(id=shiftbaggingoff_id)
        return ShiftDetailsBaggingOff.objects.create(shiftbaggingoff=shiftbaggingoff, **validated_data)
