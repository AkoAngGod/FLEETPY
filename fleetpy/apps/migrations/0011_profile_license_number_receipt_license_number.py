# Generated by Django 5.1 on 2024-12-02 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0010_taxi'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='license_number',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='receipt',
            name='license_number',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]