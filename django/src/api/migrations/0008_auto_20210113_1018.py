# Generated by Django 3.1.5 on 2021-01-13 01:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20210113_1016'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='order_date',
            new_name='order_data',
        ),
    ]
