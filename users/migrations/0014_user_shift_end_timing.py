# Generated by Django 5.0.6 on 2024-11-13 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_remove_user_employee_tax_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='shift_end_timing',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
