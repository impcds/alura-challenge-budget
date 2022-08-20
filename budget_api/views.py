from rest_framework import viewsets, generics
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


class DespesasMesViewList(generics.ListAPIView):
    """Exibir as despesas de determinado mes de um ano"""
    def get_queryset(self):
        queryset = Despesa.objects.filter(data__year=self.kwargs['year'], data__month=self.kwargs['month'])
        return queryset

    serializer_class = DespesaSerializer


class ReceitasMesViewList(generics.ListAPIView):
    """Exibir as receitas de um determinado mes do ano"""
    def get_queryset(self):
        queryset = Receita.objects.filter(data__year=self.kwargs['year'], data__month=self.kwargs['month'])
        return queryset

    serializer_class = ReceitaSerializer
