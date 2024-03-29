# Generated by Django 4.2.1 on 2024-01-22 15:26

import API.models
from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TranSport_API',
            fields=[
                ('transport_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('transport_code', models.CharField(default='150de874fa7d1a9e', max_length=16)),
                ('product_name', models.CharField(default='', max_length=2000)),
                ('quantity', models.IntegerField(default=0)),
                ('weight', models.FloatField(default=0)),
                ('transport_price', models.FloatField(default=15000)),
                ('status', models.CharField(choices=[('Đã Nhận Đơn', 'Đã Nhận Đơn'), ('Đang Vận Chuyển', 'Đang Vận Chuyển'), ('Giao Hàng Thành Công', 'Giao Hàng Thành Công')], default='Đã Nhận Đơn', max_length=20)),
                ('name_ownerShop', models.CharField(default='', max_length=200)),
                ('from_district', models.CharField(blank=True, max_length=200)),
                ('from_province', models.CharField(blank=True, max_length=200)),
                ('name_customer', models.CharField(default='', max_length=200)),
                ('description', models.CharField(default='', max_length=2000, null=True)),
                ('customer_phone', models.CharField(default='', max_length=20)),
                ('to_district', models.CharField(blank=True, max_length=200)),
                ('to_province', models.CharField(blank=True, max_length=200)),
                ('expected_date', models.DateField(default=API.models.default_expected_date)),
                ('created_at', models.DateField(default=django.utils.timezone.now)),
                ('updated_at', models.DateField(default=django.utils.timezone.now)),
            ],
        ),
    ]
