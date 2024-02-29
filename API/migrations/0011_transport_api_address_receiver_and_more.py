# Generated by Django 4.2.1 on 2024-02-26 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0010_alter_transport_api_transport_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='transport_api',
            name='address_receiver',
            field=models.CharField(default='', max_length=2000),
        ),
        migrations.AddField(
            model_name='transport_api',
            name='address_sender',
            field=models.CharField(default='', max_length=2000),
        ),
        migrations.AlterField(
            model_name='transport_api',
            name='transport_code',
            field=models.CharField(default='8a052e95c26106d0', max_length=16),
        ),
    ]