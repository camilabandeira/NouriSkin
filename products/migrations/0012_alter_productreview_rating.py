# Generated by Django 5.1.3 on 2024-12-18 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_alter_productreview_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productreview',
            name='rating',
            field=models.DecimalField(decimal_places=1, max_digits=2),
        ),
    ]
