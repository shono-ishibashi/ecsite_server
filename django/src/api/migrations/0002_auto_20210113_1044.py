# Generated by Django 3.1.5 on 2021-01-13 01:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='Order',
            old_name='order_data',
            new_name='order_date'
        )
    ]
