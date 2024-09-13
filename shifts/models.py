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
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.shift_no:
            # Get the maximum shift_no value from the existing records
            max_shift_no = Shift.objects.aggregate(Max('shift_no'))['shift_no__max']
            # If there are no existing records, start with 1, otherwise increment by 1
            self.shift_no = 1 if max_shift_no is None else max_shift_no + 1
        super(Shift, self).save(*args, **kwargs)

    def __str__(self):
        return f"Shift {self.shift_no}"

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

