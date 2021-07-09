# Generated by Django 3.1.5 on 2021-02-07 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0005_stock_pctgainformatted'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='perfToday',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=1000),
        ),
        migrations.AddField(
            model_name='stock',
            name='prevClose',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=1000),
        ),
    ]
