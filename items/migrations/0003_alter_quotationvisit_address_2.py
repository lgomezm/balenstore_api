# Generated by Django 5.0.3 on 2024-03-29 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0002_alter_quotationvisit_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotationvisit',
            name='address_2',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
