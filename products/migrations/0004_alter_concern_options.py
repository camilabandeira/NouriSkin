# Generated by Django 5.1.3 on 2024-12-14 11:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_rename_concerns_concern_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='concern',
            options={'verbose_name_plural': 'Concerns'},
        ),
    ]