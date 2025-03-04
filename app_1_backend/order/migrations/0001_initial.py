# Generated by Django 5.1.1 on 2024-10-26 11:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('extras', '0002_alter_address_addresstype'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_id', models.CharField(max_length=255)),
                ('order_products', models.JSONField(default=list)),
                ('rated', models.JSONField(default=list)),
                ('total_quantity', models.IntegerField()),
                ('subtotal', models.IntegerField()),
                ('total', models.IntegerField()),
                ('delivery_status', models.CharField(choices=[('đang chờ xử lý', 'Đang chờ xử lý'), ('đã giao', 'Đã giao'), ('đã hủy', 'Đã hủy')], default='đang chờ xử lý', max_length=255)),
                ('payment_status', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='extras.address')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
