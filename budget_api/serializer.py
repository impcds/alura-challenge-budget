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


# class ResumoMesSerializer(serializers.Serializer):
#     receitas = serializers.DecimalField(max_digits=11, decimal_places=2)
#     despesas= serializers.DecimalField(max_digits=11, decimal_places=2)
#     saldo = serializers.DecimalField(max_digits=11, decimal_places=2)
