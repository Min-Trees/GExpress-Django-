# Generated by Django 4.2.1 on 2024-02-24 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0009_alter_transport_api_transport_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transport_api',
            name='transport_code',
            field=models.CharField(default='b80180a8479a371a', max_length=16),
        ),
    ]
