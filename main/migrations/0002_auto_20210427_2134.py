# Generated by Django 3.2 on 2021-04-27 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tour',
            name='duration',
            field=models.TextField(null=False, default=0, verbose_name='Duration of the tour'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tour',
            name='price',
            field=models.IntegerField(null=False, default=0, verbose_name='Price of the tour'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tour',
            name='price_include',
            field=models.TextField(null=False, default='None', verbose_name='Prices include'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tour',
            name='type',
            field=models.TextField(null=False, default='None', verbose_name='Type of the tour'),
            preserve_default=False,
        ),
    ]
