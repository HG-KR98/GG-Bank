# Generated by Django 4.2.13 on 2024-05-23 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financial_products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='depositproducts',
            name='max_limit',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='savingproducts',
            name='max_limit',
            field=models.FloatField(null=True),
        ),
    ]
