# Generated by Django 5.1.1 on 2025-02-12 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0002_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
