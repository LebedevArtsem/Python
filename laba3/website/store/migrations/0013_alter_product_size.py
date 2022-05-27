# Generated by Django 4.0.4 on 2022-05-26 22:21

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_alter_product_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='size',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=4, null=True, verbose_name='Размер'), blank=True, null=True, size=5),
        ),
    ]
