# Generated by Django 4.1.6 on 2023-03-16 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0021_alter_shares_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shares',
            old_name='price',
            new_name='c',
        ),
        migrations.AddField(
            model_name='shares',
            name='d',
            field=models.FloatField(blank=True, default=1.0, null=True),
        ),
        migrations.AddField(
            model_name='shares',
            name='h',
            field=models.FloatField(blank=True, default=100.0, null=True),
        ),
        migrations.AddField(
            model_name='shares',
            name='l',
            field=models.FloatField(blank=True, default=100.0, null=True),
        ),
    ]
