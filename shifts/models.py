from django.db import models
from accounts.models import CustomUser

# Create your models here.

class Shift(models.Model):
    shift_no=models.IntegerField()
    activity=models.CharField(max_length=255)
    date=models.DateField()
    supplier=models.CharField(max_length=255)
    shift_type=models.CharField(max_length=255)
    coffee_type=models.CharField(max_length=255)
    output_batchno=models.IntegerField()
    location_of_batch=models.CharField(max_length=255)
    created_by=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now=True)


class ShiftDetails(models.Model):
    shift=models.ForeignKey(Shift,on_delete=models.CASCADE)

    grade=models.CharField(max_length=50)
    total_kgs=models.IntegerField()
    total_bags=models.IntegerField()
    batchno_grn=models.CharField(max_length=255)
    cell=models.CharField(max_length=50)
    entry_type=models.CharField(max_length=255)

