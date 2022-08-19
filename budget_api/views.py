from rest_framework import viewsets
from budget_api.models import Despesa, Receita
from budget_api.serializer import DespesaSerializer, ReceitaSerializer
class DespesaViewSet(viewsets.ModelViewSet):


    """Exibir todas as despesas"""
    queryset = Despesa.objects.all()
    serializer_class = DespesaSerializer
    filterset_fields = ['descricao',]


class ReceitaViewSet(viewsets.ModelViewSet):
    """Exibir todas as receitas"""
    queryset = Receita.objects.all()
    serializer_class = ReceitaSerializer
    filterset_fields = ['descricao', ]
