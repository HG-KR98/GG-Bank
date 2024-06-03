# Generated by Django 4.2.13 on 2024-05-23 06:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DepositProducts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fin_co_no', models.TextField()),
                ('dcls_month', models.TextField()),
                ('fin_prdt_cd', models.TextField(unique=True)),
                ('kor_co_nm', models.TextField()),
                ('fin_prdt_nm', models.TextField()),
                ('join_way', models.TextField()),
                ('mtrt_int', models.TextField()),
                ('spcl_cnd', models.TextField()),
                ('join_deny', models.TextField()),
                ('join_member', models.TextField()),
                ('etc_note', models.TextField()),
                ('max_limit', models.IntegerField(null=True)),
                ('dcls_strt_day', models.TextField()),
                ('dcls_end_day', models.TextField(null=True)),
                ('fin_co_subm_day', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='SavingProducts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fin_co_no', models.TextField()),
                ('dcls_month', models.TextField()),
                ('fin_prdt_cd', models.TextField(unique=True)),
                ('kor_co_nm', models.TextField()),
                ('fin_prdt_nm', models.TextField()),
                ('join_way', models.TextField()),
                ('mtrt_int', models.TextField()),
                ('spcl_cnd', models.TextField()),
                ('join_deny', models.TextField()),
                ('join_member', models.TextField()),
                ('etc_note', models.TextField()),
                ('max_limit', models.IntegerField(null=True)),
                ('dcls_strt_day', models.TextField()),
                ('dcls_end_day', models.TextField(null=True)),
                ('fin_co_subm_day', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='SavingOptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dcls_month', models.TextField()),
                ('fin_co_no', models.TextField()),
                ('fin_prdt_cd', models.TextField()),
                ('intr_rate_type', models.TextField()),
                ('intr_rate_type_nm', models.TextField()),
                ('rsrv_type', models.TextField()),
                ('rsrv_type_nm', models.TextField()),
                ('save_trm', models.TextField()),
                ('intr_rate', models.FloatField(null=True)),
                ('intr_rate2', models.FloatField(null=True)),
                ('saving_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='financial_products.savingproducts')),
            ],
        ),
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_kind', models.TextField()),
                ('fin_prdt_nm', models.TextField()),
                ('fin_prdt_cd', models.TextField()),
                ('kor_co_nm', models.TextField()),
                ('tweleve_month', models.FloatField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DepositOptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dcls_month', models.TextField()),
                ('fin_co_no', models.TextField()),
                ('fin_prdt_cd', models.TextField()),
                ('intr_rate_type', models.TextField()),
                ('intr_rate_type_nm', models.TextField()),
                ('save_trm', models.TextField()),
                ('intr_rate', models.FloatField(null=True)),
                ('intr_rate2', models.FloatField(null=True)),
                ('deposit_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='financial_products.depositproducts')),
            ],
        ),
    ]