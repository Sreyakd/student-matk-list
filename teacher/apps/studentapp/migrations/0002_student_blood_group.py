# Generated by Django 4.1.7 on 2023-10-12 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='blood_group',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
