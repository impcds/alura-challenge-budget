
from rest_framework import serializers, generics
from budget_api.models import Despesa, Receita
from django.contrib.auth.models import User

class DespesaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Despesa
        fields = ['descricao', 'valor', 'data', 'categoria']


class ReceitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receita
        fields = ['descricao', 'valor', 'data']


class CriarUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email')

        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True}
    }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
