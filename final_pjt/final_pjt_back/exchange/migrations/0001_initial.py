# Generated by Django 4.2.13 on 2024-05-23 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Exchange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cur_unit', models.CharField(max_length=100)),
                ('ttb', models.FloatField()),
                ('tts', models.FloatField()),
                ('kftc_deal_bas_r', models.FloatField()),
            ],
        ),
    ]
