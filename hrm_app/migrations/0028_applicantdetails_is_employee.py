# Generated by Django 4.1.4 on 2024-11-02 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrm_app', '0027_applicantdetails_emergency_contact_relation'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicantdetails',
            name='is_employee',
            field=models.BooleanField(default=False),
        ),
    ]
