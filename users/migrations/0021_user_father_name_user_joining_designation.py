# Generated by Django 4.1.4 on 2024-12-24 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0020_user_joining_time_salary_user_personal_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='father_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='joining_designation',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
