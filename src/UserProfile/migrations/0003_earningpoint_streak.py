# Generated by Django 4.2.2 on 2023-07-13 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserProfile', '0002_remove_earningpoint_session_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='earningpoint',
            name='streak',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
