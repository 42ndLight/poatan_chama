# Generated by Django 5.1.7 on 2025-04-02 16:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payout', '0003_payoutcycle_period'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payout',
            name='cycle',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='payout.payoutcycle'),
        ),
    ]
