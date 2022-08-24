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
                    'Total receitas': f'{receitas:.2f}',
                    'Saldo': f'{receitas:.2f}'
                }
            )

        desp_cat = despesas_query.values('categoria').annotate(Sum('valor'))
        desp_cat = {categoria['categoria'].title(): f"{categoria['valor__sum']:.2f}" for categoria in desp_cat}

        if not receitas:
            despesas = {'Total despesas': f'{despesas:.2f}', 'Saldo': f'{-despesas:.2f}'}
            despesas.update(desp_cat)

            return Response(despesas)

        saldo = receitas - despesas

        res = {'Total receitas': f'{receitas:.2f}',
                'Total despesas': f'{despesas:.2f}',
                'Saldo': f'{saldo:.2f}'}
        res.update(desp_cat)

        return Response(res)

