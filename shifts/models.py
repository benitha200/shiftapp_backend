from django.db import models
from accounts.models import CustomUser
from django.db.models import Max
# Create your models here.

class Shift(models.Model):
    shift_no = models.IntegerField(unique=True, editable=False)
    activity = models.CharField(max_length=255)
    date = models.DateField()
    supplier = models.CharField(max_length=255)
    shift_type = models.CharField(max_length=255)
    coffee_type = models.CharField(max_length=255)
    output_batchno = models.IntegerField()
    location_of_batch = models.CharField(max_length=255)
    status = models.BooleanField(default=False)
    crop_year=models.IntegerField(default=2024)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.shift_no:
            # Get the maximum shift_no value from Shift and ShiftBaggingOff
            max_shift_no = max(
                Shift.objects.aggregate(Max('shift_no'))['shift_no__max'] or 0,
                ShiftBaggingOff.objects.aggregate(Max('shift_no_bagging_off'))['shift_no_bagging_off__max'] or 0
            )
            # Increment by 1
            self.shift_no = max_shift_no + 1
        super(Shift, self).save(*args, **kwargs)

    def __str__(self):
        return f"Shift {self.shift_no}"



class ShiftDetails(models.Model):
    shift=models.ForeignKey(Shift,on_delete=models.CASCADE)
    grade=models.CharField(max_length=50)
    total_kgs=models.IntegerField()
    total_bags=models.IntegerField()
    batchno_grn=models.CharField(max_length=255)
    cell=models.CharField(max_length=50)
    entry_type=models.CharField(max_length=255)

class ShiftBaggingOff(models.Model):
    shift_no_bagging_off = models.IntegerField(unique=True, editable=False)
    activity = models.CharField(max_length=255)
    date = models.DateField()
    status = models.BooleanField(default=False)
    crop_year=models.IntegerField(default=2024)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.shift_no_bagging_off:
            max_shift_no = max(
                Shift.objects.aggregate(Max('shift_no'))['shift_no__max'] or 0,
                ShiftBaggingOff.objects.aggregate(Max('shift_no_bagging_off'))['shift_no_bagging_off__max'] or 0
            )
            self.shift_no_bagging_off = max_shift_no + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Shift {self.shift_no_bagging_off}"



class ShiftDetailsBaggingOff(models.Model):
    shiftbaggingoff=models.ForeignKey(ShiftBaggingOff,on_delete=models.CASCADE)
    grade=models.CharField(max_length=50)
    total_kgs=models.IntegerField()
    total_bags=models.IntegerField()
    balance=models.IntegerField()
    loss=models.IntegerField(default=0)
    supplier = models.CharField(max_length=255)
    cell = models.CharField(max_length=255)
    stock_card = models.CharField(max_length=255)
    lot_no = models.CharField(max_length=255,default=0)
    batchno_grn=models.CharField(max_length=255,default=67)
    parch_grade=models.CharField(max_length=255)
    year=models.IntegerField()
    entry_type=models.CharField(max_length=255)

