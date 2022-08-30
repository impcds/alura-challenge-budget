from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from budget_api.models import Despesa
from budget_api.serializer import DespesaSerializer
from datetime import date



class DespesaTestCase(APITestCase):
    def setUp(self):
        usuario = User.objects.create_user('pc', password='senha123')
        self.client.force_authenticate(user=usuario)

        self.list_url = reverse('Despesas-list')

        self.despesa1 = Despesa.objects.create(
            usuario = usuario,
            descricao='Despesa de teste',
            valor=11.00,
            # data="2022-08-23",
            data = date(2022, 8, 23),
            categoria="outros"
        )
        self.despesa2 = Despesa.objects.create(
            usuario = usuario,
            descricao='Gastei dinheiro',
            valor=50.00,
            # data="2022-08-23",
            data = date(2022, 8, 23),
            categoria="lazer"
        )

    def test_requisicao_get_listar_despesas(self):
        """Teste para verificar requisição GET para listar todas as despesas"""
        response = self.client.get(self.list_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_requisicao_post_nova_despesa(self):
        """Teste para verificar requisição POST para uma nova despesa"""
        data = {
            "descricao": "Despesa de teste",
            "valor": 20.0,
            "data": "2022-09-23",
            "categoria": "outros"
        }
        response = self.client.post(self.list_url, data=data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_despesa_descricao_repetida(self):
        """Teste para aferir a criação de despesa única no mês"""
        data = {
            "descricao": "Despesa de teste",
            "valor": 20.0,
            "data": "2022-08-23",
            "categoria": "outros"
        }
        response = self.client.post(self.list_url, data=data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_requisicao_put_edicao_de_despesa(self):
        """Teste para verificar a edição de uma despesa com o metodo PUT"""
        data = {
            "descricao": "Despesa de teste",
            "valor": 20.0,
            "data": "2022-08-23",
            "categoria": "outros"
        }
        response = self.client.put('/despesas/1/', data=data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_requisicao_delete_despesa(self):
        """Teste para verificar a exlusão de uma despesa com o metodo DELETE"""
        response = self.client.delete('/despesas/1/')
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_despesas_mes(self):
        """Teste que verificar a requisição GET para despesas de um determinado mês"""
        response = self.client.get('/despesas/2022/8/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_get_descricao(self):
        """Teste para verificar requisição GET com parametro de busca"""
        response = self.client.get('/despesas/?descricao=teste')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_retorno_get_descricao(self):
        """Teste para verificar o conteudo retornado pela busca por descrição"""
        response = self.client.get('/despesas/?descricao=teste')
        self.assertEquals(response.data[0]['descricao'], 'Despesa de teste')

    def test_quantidade_retorno(self):
        """Teste que verifica o número de objetos JSON retornados"""
        response = self.client.get(self.list_url)
        self.assertEquals(len(response.data), 2)

    def test_fail_criar_despesa_sem_descricao(self):
        """Teste que falha ao tentar criar uma despesa sem descrição"""
        data = {"valor": 100, "data": "2022-08-20", "categoria": "outros"}
        response = self.client.post(self.list_url, data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fail_criar_despesa_sem_valor(self):
        """Teste que falha ao tentar criar uma despesa sem valor"""
        data = {"descricao": "Teste sem valor", "data": "2022-08-20", "categoria": "outros"}
        response = self.client.post(self.list_url, data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fail_criar_despesa_com_categoria_invalida(self):
        """Teste que falha ao tentar criar uma despesa em uma categoria inexistente"""
        data = {"descricao": "Categoria errada", "valor": 2, "data": "2022-08-20", "categoria": "ops"}
        response = self.client.post(self.list_url, data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)


class DespesaSerializerTestCase(TestCase):
    def setUp(self):
        self.despesa = Despesa(descricao='despesa de teste', valor=25, data='2022-08-20', categoria='lazer')
        self.serializer = DespesaSerializer(instance=self.despesa)

    def test_que_verifica_os_campos_serializados(self):
        """Teste para verificar se os campos serializados correspondem aos campos esperados"""
        data = self.serializer.data
        self.assertEquals(set(data.keys()), set(['descricao', 'valor', 'data', 'categoria']))

    def test_que_verifica_os_valores_dos_campos_serializados(self):
        """Teste para verificar se o conteúdo dos campos estão corretos"""
        data = self.serializer.data
        self.assertEquals(set(data.values()), set(['despesa de teste', '25.00', '2022-08-20', 'lazer']))
