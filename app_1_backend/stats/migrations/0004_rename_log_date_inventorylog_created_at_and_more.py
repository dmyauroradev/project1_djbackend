# Generated by Django 5.1.3 on 2024-12-02 00:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0003_rename_created_at_inventorylog_log_date_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inventorylog',
            old_name='log_date',
            new_name='created_at',
        ),
        migrations.RemoveField(
            model_name='inventorylog',
            name='description',
        ),
        migrations.AddField(
            model_name='inventorylog',
            name='remaining_quantity',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
