# Generated by Django 5.1.7 on 2025-04-01 00:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashpool', '0004_cashpool_updated_at'),
        ('transactions', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LedgerEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField(max_length=100, unique=True)),
                ('transaction_type', models.CharField(choices=[('contribution', 'Contribution'), ('payout', 'Payout'), ('adjustment', 'Adjustment')], max_length=20)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('entry_type', models.CharField(choices=[('debit', 'Debit'), ('credit', 'Credit')], max_length=10)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('account', models.CharField(max_length=50)),
                ('reference_id', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('metadata', models.JSONField(default=dict)),
                ('chama', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cashpool.chama')),
                ('initiated_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='ledger_entries', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.DeleteModel(
            name='Ledger',
        ),
        migrations.AddIndex(
            model_name='ledgerentry',
            index=models.Index(fields=['chama', 'user'], name='transaction_chama_i_ea59b9_idx'),
        ),
        migrations.AddIndex(
            model_name='ledgerentry',
            index=models.Index(fields=['transaction_type'], name='transaction_transac_df1016_idx'),
        ),
        migrations.AddIndex(
            model_name='ledgerentry',
            index=models.Index(fields=['timestamp'], name='transaction_timesta_997e42_idx'),
        ),
    ]
