# Generated by Django 5.0.6 on 2024-11-29 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_ips'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ips',
            name='ip',
            field=models.CharField(max_length=222, unique=True),
        ),
    ]
