# Generated by Django 4.1.7 on 2023-10-12 12:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0013_remove_user_admission_date_remove_user_current_class_and_more'),
        ('studentapp', '0005_student_caste'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='roll_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='student.user'),
            preserve_default=False,
        ),
    ]
