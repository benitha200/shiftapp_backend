from django.db import models

# Create your models here.

class Shift(models.Model):
    shift_no=models.IntegerField()
    activity=models.CharField(max_length=255)
    date=models.DateField()
    created_at=models.DateTimeField(auto_now=True)


class ShiftDetails(models.Model):
    shift=models.ForeignKey(Shift,on_delete=models.CASCADE)
    supplier=models.CharField(max_length=255)
    grade=models.CharField(max_length=50)
    total_kgs=models.IntegerField()
    total_bags=models.IntegerField()
    batchno_grn=models.CharField(max_length=255)
    cell=models.CharField(max_length=50)
    entry_type=models.CharField(max_length=255)

