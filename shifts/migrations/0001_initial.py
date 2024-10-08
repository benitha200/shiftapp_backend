# Generated by Django 5.1 on 2024-08-19 14:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Shift',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shift_no', models.IntegerField()),
                ('activity', models.CharField(max_length=255)),
                ('date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ShiftDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('supplier', models.CharField(max_length=255)),
                ('grade', models.CharField(max_length=50)),
                ('total_kgs', models.IntegerField()),
                ('total_bags', models.IntegerField()),
                ('batchno_grn', models.CharField(max_length=255)),
                ('cell', models.CharField(max_length=50)),
                ('entry_type', models.CharField(max_length=255)),
                ('shift', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shifts.shift')),
            ],
        ),
    ]
