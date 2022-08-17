import django.db.utils
from django.db import models
from datetime import date
from django.http import HttpResponse


class Despesa(models.Model):
    descricao = models.CharField(max_length=255, unique_for_month='data')
    valor = models.DecimalField(max_digits=9, decimal_places=2)
    data = models.DateField(default=date.today)

    def __str__(self):
        return self.descricao


class Receita(models.Model):
    descricao = models.CharField(max_length=255, unique_for_month='data')
    valor = models.DecimalField(max_digits=9, decimal_places=2)
    data = models.DateField(default=date.today)

    def __str__(self):
        return self.descricao
