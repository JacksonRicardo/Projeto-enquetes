from django.test import TestCase
from django.utils import timezone
import datetime
from .models import Pergunta

### Testes unitários para a classe de modelo Pergunta
#####################################################
class PerguntaModelTests(TestCase):
    def test_publicada_recentemente_com_data_no_futuro(self):
        """
        Testar se o método publicada_recentemente() retorna False para
        perguntas com data de publicação no futuro.
        """
        data = timezone.now() + datetime.timedelta(seconds=1)
        pergunta_no_futuro = Pergunta(data_publicacao=data)
        self.assertIs(pergunta_no_futuro.publicada_recentemente(), False)

    def test_publicada_recentemente_com_data_alem_das_ultimas_24hs(self):
        """
        Testar se o método publicada_recentemente() retorna False para data
        de publicação mais antiga que às últimas 24hs.
        """
        data = timezone.now() - datetime.timedelta(days=1, seconds=1)
        pergunta_no_passado = Pergunta(data_publicacao=data)
        self.assertIs(pergunta_no_passado.publicada_recentemente(), False)

    def test_publicada_recentemente_com_data_nas_ultimas_24hs(self):
        """
        Testar se o método publicada_recentemente() retorna True para data
        de publicação dentro do intervalo das últimas 24hs e o instante atual.
        """
        data = timezone.now()-datetime.timedelta(hours=23,minutes=59,seconds=59)
        data2 = timezone.now()-datetime.timedelta(seconds=1)
        pergunta_recente = Pergunta(data_publicacao=data)
        pergunta_recente2 = Pergunta(data_publicacao=data2)
        self.assertIs(pergunta_recente.publicada_recentemente(), True)
        self.assertIs(pergunta_recente2.publicada_recentemente(), True)
