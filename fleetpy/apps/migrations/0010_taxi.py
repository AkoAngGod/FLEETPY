# Generated by Django 5.1 on 2024-12-02 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0009_remove_receipt_driver_receipt_driver_firstname_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Taxi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plate_number', models.CharField(max_length=7, unique=True)),
            ],
        ),
    ]