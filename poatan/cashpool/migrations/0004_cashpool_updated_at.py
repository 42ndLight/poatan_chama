# Generated by Django 5.1.7 on 2025-03-24 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashpool', '0003_rename_chama_name_chama_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='cashpool',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
