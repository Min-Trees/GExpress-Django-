# Generated by Django 4.2.1 on 2024-02-28 03:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Application', '0004_district_province_delete_alldistrict_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='role',
        ),
    ]