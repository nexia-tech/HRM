# Generated by Django 5.0.6 on 2024-08-03 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrm_app', '0012_screenshotrecords'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendancemodel',
            name='break_time_stamp',
            field=models.ManyToManyField(blank=True, to='hrm_app.employeebreakrecords'),
        ),
    ]
