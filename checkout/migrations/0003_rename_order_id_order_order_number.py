# Generated by Django 5.1.3 on 2024-12-23 13:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0002_order_delivery_cost'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='order_id',
            new_name='order_number',
        ),
    ]
