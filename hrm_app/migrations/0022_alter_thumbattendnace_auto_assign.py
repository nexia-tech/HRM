# Generated by Django 5.0.6 on 2024-10-22 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrm_app', '0021_thumbattendnace_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thumbattendnace',
            name='auto_assign',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]