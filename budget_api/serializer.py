from rest_framework import serializers
from budget_api.models import Despesa, Receita


class DespesaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Despesa
        exclude = ['id']


class ReceitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receita
        fields = ['descricao', 'valor', 'data']
