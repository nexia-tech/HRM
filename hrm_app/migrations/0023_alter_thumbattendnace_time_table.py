# Generated by Django 5.0.6 on 2024-10-22 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrm_app', '0022_alter_thumbattendnace_auto_assign'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thumbattendnace',
            name='time_table',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
