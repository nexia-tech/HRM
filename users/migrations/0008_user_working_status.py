# Generated by Django 5.0.6 on 2024-10-23 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_user_educational_certificates_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='working_status',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]