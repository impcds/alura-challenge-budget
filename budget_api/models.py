import django.db.utils
from django.db import models
from datetime import date
from django.http import HttpResponse, request, HttpRequest
from rest_framework import serializers


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

    usuario = models.ForeignKey('auth.User', related_name='despesas', on_delete=models.CASCADE)
    descricao = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=9, decimal_places=2)
    data = models.DateField(default=date.today)
    categoria = models.CharField(max_length=11, choices=CATEGORIAS, default='outros')

    def save(self, *args, **kwargs):
        if Despesa.objects.filter(descricao__exact=self.descricao, data__month=self.data.month,
                                       data__year=self.data.year, usuario=self.usuario):
            raise serializers.ValidationError("Despesa duplicada no mês!")
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return self.descricao


class Receita(models.Model):
    usuario = models.ForeignKey('auth.User', related_name='receitas', on_delete=models.CASCADE)
    descricao = models.CharField(max_length=255, unique_for_month='data')
    valor = models.DecimalField(max_digits=9, decimal_places=2)
    data = models.DateField(default=date.today)

    def save(self, *args, **kwargs):
        if Receita.objects.filter(descricao__exact=self.descricao, data__month=self.data.month,
                                       data__year=self.data.year, usuario=self.usuario):
            raise serializers.ValidationError("Receita duplicada no mês!")
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return self.descricao
