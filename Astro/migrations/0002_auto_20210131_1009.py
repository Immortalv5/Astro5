# Generated by Django 3.0.3 on 2021-01-31 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Astro', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='checksum',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='order_id',
            field=models.CharField(blank=True, max_length=500, null=True, unique=True),
        ),
    ]
