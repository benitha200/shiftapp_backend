# Generated by Django 5.1 on 2024-09-11 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shifts', '0003_shift_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shift',
            name='shift_no',
            field=models.IntegerField(editable=False, unique=True),
        ),
    ]
