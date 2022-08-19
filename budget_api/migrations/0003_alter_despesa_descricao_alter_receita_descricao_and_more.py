# Generated by Django 4.1 on 2022-08-17 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget_api', '0002_alter_despesa_descricao_alter_receita_descricao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='despesa',
            name='descricao',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='receita',
            name='descricao',
            field=models.CharField(max_length=255),
        ),
        migrations.AddConstraint(
            model_name='despesa',
            constraint=models.UniqueConstraint(fields=('descricao', 'data'), name='descricao_unica_por_mes'),
        ),
    ]