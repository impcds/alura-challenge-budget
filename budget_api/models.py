import django.db.utils
from django.db import models
from datetime import date
from django.http import HttpResponse


class Despesa(models.Model):
    CATEGORIAS = [
        ('alimentacao', 'Alimentação'),
        ('saude', 'Saúde'),
        ('moradia', 'Moradia'),
        ('transporte', 'Transporte'),
        ('educacao', 'Educaçao'),
        ('lazer', 'Lazer'),
        ('imprevistos', 'Imprevistos'),
        ('outros', 'Outros')
    ]

    descricao = models.CharField(max_length=255, unique_for_month='data')
    valor = models.DecimalField(max_digits=9, decimal_places=2)
    data = models.DateField(default=date.today)
    categoria = models.CharField(max_length=11, choices=CATEGORIAS, default='outros')

    def __str__(self):
        return self.descricao


class Receita(models.Model):
    descricao = models.CharField(max_length=255, unique_for_month='data')
    valor = models.DecimalField(max_digits=9, decimal_places=2)
    data = models.DateField(default=date.today)

    def __str__(self):
        return self.descricao
