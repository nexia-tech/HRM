# Generated by Django 5.0.6 on 2024-10-18 17:52

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrm_app', '0017_alter_applicantdetails_email_address'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SystemAttendanceModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shift_date', models.DateField()),
                ('shift_start_time', models.TimeField(null=True)),
                ('time_out_time', models.TimeField(blank=True, null=True)),
                ('remaining_hours', models.DurationField(default=datetime.timedelta(seconds=28800))),
                ('is_present', models.BooleanField(default=True)),
                ('is_time_out_marked', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('employee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
