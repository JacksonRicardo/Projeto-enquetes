from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
import datetime
from .models import Pergunta

def criar_pergunta(texto, dias):
    """
    Cria uma um objeto pergunta informando um texto e uma quantidade de dias,
    a qual pode ser posiva (futuro) ou negativa (passado) a partir do dia atual.
    """
    data = timezone.now() + datetime.timedelta(days = dias)
    return Pergunta.objects.create(texto = texto, data_publicacao = data)

#### Testes funcionais referentes à classe DetalhesView
#######################################################
class DetalhesViewTest(TestCase):
    def test_detalhes_de_pergunta_com_data_de_publicacao_no_futuro(self):
        """
        Esperado que retorne um erro 404 ao tentar exibir detalhes de uma
        pergunta com data de publicação no futuro.
        """
        p1 = criar_pergunta(texto='Pergunta no futuro', dias=5)
        resposta = self.client.get(reverse('enquetes:detalhes', args=(p1.id,)))
        self.assertEqual(resposta.status_code, 404)

    def test_detalhes_de_pergunta_com_data_de_publicacao_no_passado(self):
        """
        Esperada a exibição normal de uma pergunta com data de publicação
        no pssado.
        """
        p2 = criar_pergunta(texto='Pergunta no passado', dias=-5)
        resposta = self.client.get(reverse('enquetes:detalhes', args=(p2.id,)))
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, p2.texto)

    def test_detalhes_informando_identificador_inexistente(self):
        """
        Esperado um erro 404 quando informadro um identificador inválido.
        """
        resposta = self.client.get(reverse('enquetes:detalhes', args=(99,)))
        self.assertEqual(resposta.status_code, 404)

#### Testes funcionais referentes a classe ViewIndex
####################################################
class IndexViewTest(TestCase):
    def test_sem_perguntas_cadastradas(self):
        """
        Não existindo perguntas cadastradas é exibida uma mensagem específica.
        """
        resposta = self.client.get(reverse('enquetes:index'))
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "Nenhuma enquete cadastrada até o momento!")
        self.assertQuerysetEqual(resposta.context['lista_perguntas'], [])

    def test_com_pergunta_no_passado(self):
        """
        Pergunta com data de publicação no passado é exibida ao acessar a index.
        """
        criar_pergunta(texto='Pergunta no passado', dias=-30)
        resposta = self.client.get(reverse('enquetes:index'))
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "Pergunta no passado")
        self.assertQuerysetEqual(
            resposta.context['lista_perguntas'],
            ['<Pergunta: Pergunta no passado>']
        )

    def test_com_pergunta_no_futuro(self):
        """
        Pergunta com data de publicação no futuro NÃO é exibida na index.
        """
        criar_pergunta(texto='Pergunta no futuro', dias=30)
        resposta = self.client.get(reverse('enquetes:index'))
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "Nenhuma enquete cadastrada até o momento!")
        self.assertQuerysetEqual(resposta.context['lista_perguntas'], [])

    def test_pergunta_no_passado_e_outra_no_futuro(self):
        """
        A index exibe APENAS a pergunta com data de publicação no passado.
        """
        criar_pergunta(texto='Pergunta no passado', dias=-30)
        criar_pergunta(texto='Pergunta no futuro', dias=30)
        resposta = self.client.get(reverse('enquetes:index'))
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "Pergunta no passado")
        self.assertQuerysetEqual(
            resposta.context['lista_perguntas'],
            ['<Pergunta: Pergunta no passado>']
        )

    def test_duas_perguntas_no_passado(self):
        """
        São exibidas mais de uma pergunta com data de publicação no passado.
        """
        criar_pergunta(texto='Pergunta no passado 1', dias=-30)
        criar_pergunta(texto='Pergunta no passado 2', dias=-5)
        resposta = self.client.get(reverse('enquetes:index'))
        self.assertEqual(resposta.status_code, 200)
        self.assertQuerysetEqual(
            resposta.context['lista_perguntas'],
            ['<Pergunta: Pergunta no passado 2>',
            '<Pergunta: Pergunta no passado 1>']
        )
