# Generated by Django 5.1.3 on 2024-12-02 05:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0004_rename_log_date_inventorylog_created_at_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='InventoryLog',
        ),
    ]
