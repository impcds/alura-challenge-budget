# Generated by Django 4.1 on 2022-08-17 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget_api', '0003_alter_despesa_descricao_alter_receita_descricao_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='despesa',
            name='descricao_unica_por_mes',
        ),
        migrations.AddConstraint(
            model_name='despesa',
            constraint=models.UniqueConstraint(fields=('descricao', 'data'), name='descricao_unica_por_mes', violation_error_message='Nao e possivel cadastrar a mesma despesa neste mes'),
        ),
    ]
