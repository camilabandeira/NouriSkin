# Generated by Django 5.1.3 on 2024-12-14 11:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_concerns_options'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Concerns',
            new_name='Concern',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='concerns',
            new_name='concern',
        ),
    ]
