# Generated by Django 4.2.14 on 2024-07-13 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrm_app', '0010_employeebreakrecords_is_break_end'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendancemodel',
            name='time_out_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]