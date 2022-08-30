from rest_framework.test import APITestCase
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from budget_api.models import Receita
from budget_api.serializer import ReceitaSerializer
from datetime import date

class ReceitaTestCase(APITestCase):
    def setUp(self):
        usuario = User.objects.create_user('pc', password='senha123')
        self.client.force_authenticate(user=usuario)

        self.list_url = reverse('Receitas-list')

        self.receita1 = Receita.objects.create(
            usuario=usuario,
            descricao='Receita de teste',
            valor=11.00,
            data=date(2022, 8, 23)
            # data="2022-08-23"
        )
        self.receita2 = Receita.objects.create(
            usuario=usuario,
            descricao='Ganhei dinheiro',
            valor=50.00,
            data=date(2022, 8, 23)
            # data="2022-08-23"
        )

    def test_requisicao_get_listar_receitas(self):
        """Teste para verificar requisição GET para listar todas as receitas"""
        response = self.client.get(self.list_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_requisicao_post_nova_receita(self):
        """Teste para verificar requisição POST para uma nova receita"""
        data = {
            "descricao": "Receita de teste",
            "valor": 20.0,
            "data": "2022-09-23"
        }
        response = self.client.post(self.list_url, data=data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_receita_descricao_repetida(self):
        """Teste para aferir a criação de receita única no mês"""
        data = {
            "descricao": "Receita de teste",
            "valor": 20.0,
            "data": "2022-08-23"
        }
        response = self.client.post(self.list_url, data=data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_requisicao_put_edicao_de_receita(self):
        """Teste para verificar a edição de uma receita com o metodo PUT"""
        data = {
            "descricao": "Receita de teste",
            "valor": 20.0,
            "data": "2022-08-23"
        }
        response = self.client.put('/receitas/1/', data=data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_requisicao_delete_receita(self):
        """Teste para verificar a exlusão de uma receita com o metodo DELETE"""
        response = self.client.delete('/receitas/1/')
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_receitas_mes(self):
        """Teste que verificar a requisição GET para receitas de um determinado mês"""
        response = self.client.get('/receitas/2022/8/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_get_descricao(self):
        """Teste para verificar requisição GET com parametro de busca"""
        response = self.client.get('/receitas/?descricao=teste')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_retorno_get_descricao(self):
        """Teste para verificar o conteudo retornado pela busca por descrição"""
        response = self.client.get('/receitas/?descricao=teste')
        self.assertEquals(response.data[0]['descricao'], 'Receita de teste')

    def test_quantidade_retorno(self):
        """Teste que verifica o número de objetos JSON retornados"""
        response = self.client.get(self.list_url)
        self.assertEquals(len(response.data), 2)

    def test_fail_criar_receita_sem_descricao(self):
        """Teste que falha ao tentar criar uma receita sem descrição"""
        data = {"valor": 100, "data": "2022-08-20"}
        response = self.client.post(self.list_url, data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fail_criar_receita_sem_valor(self):
        """Teste que falha ao tentar criar uma receita sem valor"""
        data = {"descricao": "Teste sem valor", "data": "2022-08-20"}
        response = self.client.post(self.list_url, data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)


class ReceitaSerializerTestCase(TestCase):
    def setUp(self):
        self.receita = Receita(descricao='receita de teste', valor=25, data='2022-08-20')
        self.serializer = ReceitaSerializer(instance=self.receita)

    def test_que_verifica_os_campos_serializados(self):
        """Teste para verificar se os campos serializados correspondem aos campos esperados"""
        data = self.serializer.data
        self.assertEquals(set(data.keys()), set(['descricao', 'valor', 'data']))

    def test_que_verifica_os_valores_dos_campos_serializados(self):
        """Teste para verificar se o conteúdo dos campos estão corretos"""
        data = self.serializer.data
        self.assertEquals(set(data.values()), set(['receita de teste', '25.00', '2022-08-20']))
