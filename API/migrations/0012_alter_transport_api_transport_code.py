# Generated by Django 4.2.1 on 2024-02-28 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0011_transport_api_address_receiver_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transport_api',
            name='transport_code',
            field=models.CharField(default='81c277a68c900e2e', max_length=16),
        ),
    ]
