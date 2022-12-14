from django.db import models
from datetime import date
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
        # faz uma busca no BD para ver se existe algum registro com a mesma descricao e data para o usuario
        # que enviou a requisição
        query = Despesa.objects.filter(descricao__exact=self.descricao, data__month=self.data.month,
                                       data__year=self.data.year, usuario=self.usuario)
        # se a busca retornar algo e não existir um id na requisição, siginifca que é uma entrada duplicada
        # se houver um id, será feito o PUT para edição do registro no DB
        if query and not self.id:
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
        query = Receita.objects.filter(descricao__exact=self.descricao, data__month=self.data.month,
                                       data__year=self.data.year, usuario=self.usuario)
        if query and not self.id:
            raise serializers.ValidationError("Receita duplicada no mês!")
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return self.descricao
