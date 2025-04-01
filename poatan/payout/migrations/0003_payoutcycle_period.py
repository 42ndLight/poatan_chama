# Generated by Django 5.1.7 on 2025-04-01 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payout', '0002_payout_failure_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='payoutcycle',
            name='period',
            field=models.CharField(choices=[('fortnight', 'Fortnightly (14 days)'), ('month', 'Monthly (30 days)')], default='month', max_length=10),
        ),
    ]
