# Generated by Django 4.1 on 2022-08-17 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget_api', '0004_remove_despesa_descricao_unica_por_mes_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='despesa',
            name='valor',
            field=models.DecimalField(decimal_places=2, max_digits=9),
        ),
        migrations.AlterField(
            model_name='receita',
            name='descricao',
            field=models.CharField(max_length=255, unique_for_month='data'),
        ),
        migrations.AlterField(
            model_name='receita',
            name='valor',
            field=models.DecimalField(decimal_places=2, max_digits=9),
        ),
    ]
