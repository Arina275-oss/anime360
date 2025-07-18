# Generated by Django 5.2.4 on 2025-07-14 19:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpecialOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount_percent', models.PositiveIntegerField(verbose_name='Процент скидки')),
                ('start_date', models.DateTimeField(verbose_name='Начало акции')),
                ('end_date', models.DateTimeField(verbose_name='Конец акции')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активна')),
            ],
            options={
                'verbose_name': 'Акция',
                'verbose_name_plural': 'Акции',
                'ordering': ['-start_date'],
            },
        ),
        migrations.AddIndex(
            model_name='category',
            index=models.Index(fields=['name'], name='shop_catego_name_289c7e_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['id', 'slug'], name='shop_produc_id_f21274_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['name'], name='shop_produc_name_a2070e_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['-created'], name='shop_produc_created_ef211c_idx'),
        ),
        migrations.AddField(
            model_name='specialoffer',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='special_offers', to='shop.product', verbose_name='Товар'),
        ),
        migrations.AddIndex(
            model_name='specialoffer',
            index=models.Index(fields=['-start_date'], name='shop_specia_start_d_2264ec_idx'),
        ),
        migrations.AddIndex(
            model_name='specialoffer',
            index=models.Index(fields=['is_active'], name='shop_specia_is_acti_b7cfeb_idx'),
        ),
    ]
