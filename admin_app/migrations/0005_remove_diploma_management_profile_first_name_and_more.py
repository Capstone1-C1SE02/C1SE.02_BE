# Generated by Django 5.0.3 on 2024-05-12 10:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0004_diploma_management_profile_apporvedy_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='diploma_management_profile',
            name='FIRST_NAME',
        ),
        migrations.RemoveField(
            model_name='diploma_management_profile',
            name='LAST_NAME',
        ),
        migrations.RemoveField(
            model_name='diploma_management_profile',
            name='MIDDLE_NAME',
        ),
    ]
