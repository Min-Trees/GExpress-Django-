# Generated by Django 4.2.1 on 2024-02-23 04:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Application', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllProvince',
            fields=[
                ('id', models.IntegerField(blank=True, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='payment',
            name='cvv_pay',
            field=models.IntegerField(default='123'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='expiration_month',
            field=models.IntegerField(default='12'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='expiration_year',
            field=models.IntegerField(default='2024'),
        ),
        migrations.CreateModel(
            name='AllDistrict',
            fields=[
                ('id', models.IntegerField(blank=True, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('province', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Application.allprovince')),
            ],
        ),
    ]
