# Generated by Django 5.0.3 on 2024-05-17 12:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0006_alter_academic_intake_session_academic_program_curriculum_academic_intake_session_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='diploma_management_profile',
            old_name='APPORVEDY',
            new_name='APPORVED',
        ),
        migrations.AlterField(
            model_name='student',
            name='ACADEMIC_LEVEL_TYPE_ID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_app.academic_level_type'),
        ),
        migrations.AlterField(
            model_name='student',
            name='LEARNING_STATUS_TYPE_ID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_app.learning_status_type'),
        ),
    ]