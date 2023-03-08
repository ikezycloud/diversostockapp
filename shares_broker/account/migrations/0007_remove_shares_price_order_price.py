# Generated by Django 4.1.6 on 2023-02-15 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_order_quantity_order_shares_delete_orderitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shares',
            name='price',
        ),
        migrations.AddField(
            model_name='order',
            name='price',
            field=models.DecimalField(decimal_places=2, default=1.0, max_digits=7),
        ),
    ]
