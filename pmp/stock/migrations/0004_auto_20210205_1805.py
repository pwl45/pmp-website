# Generated by Django 3.1.5 on 2021-02-05 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0003_stock_pctgain'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='prices',
            field=models.TextField(default=''),
        ),
    ]
