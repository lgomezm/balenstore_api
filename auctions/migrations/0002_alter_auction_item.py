# Generated by Django 5.0.3 on 2024-03-29 02:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
        ('items', '0003_alter_quotationvisit_address_2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='item',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='items.item'),
        ),
    ]