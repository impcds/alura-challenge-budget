from rest_framework.test import APITestCase
from rest_framework import status
from budget_api.models import Despesa, Receita
from budget_api.serializer import DespesaSerializer
from django.contrib.auth.models import User
from datetime import date

class ResumoMesTestCase(APITestCase):
    def setUp(self):
        usuario = User.objects.create_user('pc', password='senha123')
        self.client.force_authenticate(user=usuario)


        self.despesa1 = Despesa.objects.create(
            usuario=usuario,
            descricao='Despesa de teste',
            valor=25.00,
            # data="2022-08-23",
            data = date(2022, 8, 23),
            categoria="outros"
        )
        self.despesa2 = Despesa.objects.create(
            usuario=usuario,
            descricao='Gastei dinheiro',
            valor=50.00,
            # data="2022-08-23",
            data=date(2022, 8, 23),
            categoria="lazer"
        )
        self.despesa3 = Despesa.objects.create(
            usuario=usuario,
            descricao='Gastei mais dinheiro',
            valor=10.00,
            # data="2022-08-23",
            data=date(2022, 8, 23),
            categoria="lazer"
        )
        self.despesa4 = Despesa.objects.create(
            usuario=usuario,
            descricao='Gastei mais dinheiro',
            valor=10.00,
            # data="2022-10-23",
            data=date(2022, 10, 23),
            categoria="outros"
        )
        self.receita1 = Receita.objects.create(
            usuario=usuario,
            descricao='Receita de teste',
            valor=30.00,
            data=date(2022, 8, 23)
            # data="2022-08-23"
        )
        self.receita2 = Receita.objects.create(
            usuario=usuario,
            descricao='Ganhei dinheiro',
            valor=60.00,
            data=date(2022, 8, 23)
            # data="2022-08-23"
        )
        self.receita3 = Receita.objects.create(
            usuario=usuario,
            descricao='Ganhei dinheiro',
            valor=60.00,
            data=date(2022, 9, 23)
            # data="2022-09-23"
        )

    def test_requisicao_get_resumo(self):
        """Teste para verificar requisição GET no resumo mensal"""
        response = self.client.get('/resumo/2022/8/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)


    def test_verificar_resumo(self):
        """Teste para verificar os dados retornados pela requisição GET no resumo mensal"""
        response = self.client.get('/resumo/2022/8/')
        self.assertEquals(response.data['Total receitas'], '90.00')
        self.assertEquals(response.data['Total despesas'], '85.00')
        self.assertEquals(response.data['Saldo'], '5.00')
        self.assertEquals(response.data['Lazer'], '60.00')

    def test_verificar_mes_com_apenas_receitas(self):
        """Teste para verificar o retorno de uma requisição GET para um mês com apenas receitas"""
        response = self.client.get('/resumo/2022/9/')
        self.assertEquals(set(response.data.keys()), {'Total receitas', 'Saldo'})

    def test_verificar_mes_com_apenas_despesas(self):
        """Teste para verificar o retorno de uma requisição GET para um mês com apenas despesas"""
        response = self.client.get('/resumo/2022/10/')
        self.assertEquals(set(response.data.keys()), {'Total despesas', 'Outros', 'Saldo'})

    def test_verificar_mes_sem_lancamentos(self):
        """Teste para verificar o retorno de uma requisição GET para um mês sem lançamentos"""
        response = self.client.get('/resumo/2022/12/')
        self.assertEquals(response.data['Atenção'], 'Sem entradas no mês 12 de 2022.')

