# Generated by Django 4.2.2 on 2023-07-13 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserProfile', '0004_remove_earningpoint_streak'),
    ]

    operations = [
        migrations.AddField(
            model_name='earningpoint',
            name='visit_days',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
