# Generated by Django 4.1.7 on 2023-10-12 06:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0011_remove_user_phone_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='qualification',
        ),
        migrations.DeleteModel(
            name='Qualification',
        ),
    ]
