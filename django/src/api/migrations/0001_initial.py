# Generated by Django 3.1.5 on 2021-01-28 06:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('description', models.TextField()),
                ('price_m', models.IntegerField()),
                ('price_l', models.IntegerField()),
                ('image_path', models.TextField()),
                ('deleted', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'items',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField()),
                ('total_price', models.IntegerField()),
                ('order_date', models.DateField(blank=True, null=True)),
                ('destination_name', models.CharField(blank=True, max_length=100)),
                ('destination_email', models.CharField(blank=True, max_length=100)),
                ('destination_zipcode', models.CharField(blank=True, max_length=7)),
                ('destination_address', models.CharField(blank=True, max_length=200)),
                ('destination_tel', models.CharField(blank=True, max_length=15)),
                ('delivery_time', models.DateTimeField(blank=True, null=True)),
                ('payment_method', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'orders',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('size', models.CharField(max_length=1)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='api.item')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='api.order')),
            ],
            options={
                'db_table': 'order_items',
            },
        ),
        migrations.CreateModel(
            name='Topping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('price_m', models.IntegerField()),
                ('price_l', models.IntegerField()),
            ],
            options={
                'db_table': 'toppings',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100, unique=True)),
                ('password', models.TextField()),
                ('zipcode', models.CharField(max_length=7)),
                ('address', models.CharField(max_length=200)),
                ('telephone', models.CharField(max_length=15)),
                ('status', models.CharField(default=0, max_length=1)),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='UserUtil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='util', to='api.user')),
            ],
            options={
                'db_table': 'user_utils',
            },
        ),
        migrations.CreateModel(
            name='OrderTopping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_toppings', to='api.orderitem')),
                ('topping', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_toppings', to='api.topping')),
            ],
            options={
                'db_table': 'order_toppings',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.user'),
        ),
    ]
