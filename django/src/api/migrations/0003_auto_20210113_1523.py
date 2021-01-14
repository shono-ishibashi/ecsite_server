# Generated by Django 3.1.5 on 2021-01-13 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20210113_1044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='destination_address',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='destination_email',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='destination_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='destination_tel',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='destination_zipcode',
            field=models.CharField(blank=True, max_length=7, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
