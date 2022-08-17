from django.db import models
from datetime import date


class Despesa(models.Model):
    descricao = models.CharField(max_length=255)
    valor = models.FloatField()
    data = models.DateField(default=date.today)

    def __str__(self):
        return self.descricao


class Receita(models.Model):
    descricao = models.CharField(max_length=255)
    valor = models.FloatField()
    data = models.DateField(default=date.today)

    def __str__(self):
        return self.descricao
