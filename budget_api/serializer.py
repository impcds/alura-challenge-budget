from rest_framework import serializers
from budget_api.models import Despesa, Receita


class DespesaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Despesa
        exclude = []


class ReceitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receita
        fields = '__all__'
