# Generated by Django 5.2.4 on 2025-07-16 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_student_email_subject_classroom_subject_teacher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='email',
            field=models.EmailField(default='', max_length=254),
        ),
    ]
