# Generated by Django 5.1 on 2024-12-04 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0014_remove_profile_created_at_remove_profile_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='profile_photos/'),
        ),
    ]
