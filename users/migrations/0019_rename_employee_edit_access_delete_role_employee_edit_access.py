# Generated by Django 5.0.6 on 2024-12-04 16:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_rename_applicant_edit_access_delete_role_applicant_add_access_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='role',
            old_name='employee_edit_access_delete',
            new_name='employee_edit_access',
        ),
    ]
