# Generated by Django 4.1.7 on 2023-10-10 09:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0007_alter_user_gender'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='choices',
            new_name='user_type',
        ),
    ]