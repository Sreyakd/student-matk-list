# Generated by Django 4.1.7 on 2023-10-13 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0014_alter_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='roll_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]