# Generated by Django 5.1 on 2024-08-23 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('shift_leader', 'shift_leader'), ('manager', 'Manager')], max_length=20),
        ),
    ]
