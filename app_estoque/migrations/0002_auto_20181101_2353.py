# Generated by Django 2.1.2 on 2018-11-02 01:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app_estoque', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='data_cad',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='produto',
            name='item_descricao',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='produto',
            name='min_estoque',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='entrada',
            name='data_ent',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='saida',
            name='data_sadia',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
