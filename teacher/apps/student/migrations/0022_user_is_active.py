# Generated by Django 4.1.7 on 2023-10-19 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0021_remove_user_roll_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
