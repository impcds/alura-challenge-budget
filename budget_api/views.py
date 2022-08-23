import datetime

from rest_framework import viewsets, generics, filters
from budget_api.models import Despesa, Receita
from budget_api.serializer import DespesaSerializer, ReceitaSerializer#, ResumoMesSerializer
from django.db.models import Sum
from rest_framework.response import Response


class DespesaViewSet(viewsets.ModelViewSet):
    """Exibir todas as despesas"""
    queryset = Despesa.objects.all()
    serializer_class = DespesaSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['descricao', ]
    filter_backends[0].search_param = 'descricao'


class ReceitaViewSet(viewsets.ModelViewSet):
    """Exibir todas as receitas"""
    queryset = Receita.objects.all()
    serializer_class = ReceitaSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['descricao', ]
    filter_backends[0].search_param = 'descricao'


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

class ResumoMesView(generics.ListAPIView):
    """Exibir o resumo de um mes do ano"""
    def get(self, request, year, month):
        despesas_query = Despesa.objects.filter(data__year=year, data__month=month)
        despesas = despesas_query.aggregate(Sum('valor'))['valor__sum']
        receitas = Receita.objects.filter(data__year=year, data__month=month).aggregate(Sum('valor'))['valor__sum']

        if not receitas and not despesas:
            return Response(
                {
                    'Atenção': f'Sem entradas no mês {month} de {year}.'
                }
            )
        
        if not despesas:
            return Response(
                {
                    'Receitas': receitas
                }
            )

        desp_cat = despesas_query.values('categoria').annotate(Sum('valor'))
        desp_cat = {categoria['categoria']: categoria['valor__sum'] for categoria in desp_cat}

        if not receitas:
            return Response(
                {
                    'Despesas': despesas,
                    'Categorias': desp_cat
                }
            )

        saldo = receitas - despesas

        return Response(
            {
                'Total receitas': receitas,
                'Total despesas': despesas,
                'Saldo': saldo,
                'Categorias': desp_cat
            }
        )


