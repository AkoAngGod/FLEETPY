# Generated by Django 5.1 on 2024-12-01 05:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0004_alter_profile_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('license_number', models.CharField(max_length=50)),
                ('vehicle', models.CharField(max_length=100)),
                ('time_in', models.DateTimeField(blank=True, null=True)),
                ('time_out', models.DateTimeField(blank=True, null=True)),
                ('rental_days', models.IntegerField(blank=True, null=True)),
                ('payment_amount', models.FloatField(blank=True, null=True)),
                ('total_rent', models.FloatField(blank=True, null=True)),
                ('balance', models.FloatField(blank=True, null=True)),
                ('transaction_number', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='apps.profile')),
            ],
        ),
    ]
