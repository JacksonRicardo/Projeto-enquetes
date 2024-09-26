import datetime
from django.db import models
from django.utils import timezone
from django.conf import settings

###     Clase Autor
##########################
class Autor(models.Model):
    nome = models.CharField(max_length=80)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        null = True,
    )

    class Meta:
        ordering = ['nome']
        verbose_name_plural = 'Autores'
    def __str__(self):
        return self.nome

###     Classe Perfil
###########################
class Perfil(models.Model):
    descricao = models.TextField()
    cidade = models.CharField(max_length=50)
    pais = models.CharField(max_length=30)
    genero = models.CharField(max_length=100)
    autor = models.OneToOneField(Autor, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Informações de Perfil'
    def __str__(self):
        return self.autor.nome

###     Classe Rotulo
###########################
class Rotulo(models.Model):
    titulo = models.CharField(max_length=30)

    class Meta:
        ordering = ['titulo']
        verbose_name = 'Rótulo'
        verbose_name_plural = 'Rótulos'
    def __str__(self):
        return self.titulo


###     Classe Pergunta
#############################
class Pergunta(models.Model):
    texto = models.CharField(max_length=200)
    data_publicacao = models.DateTimeField('Data de Publicação')
    data_encerramento = models.DateField('Data de Encerramento', null=True)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, null=True)
    rotulos = models.ManyToManyField(Rotulo, verbose_name='Rótulos')

    def __str__(self):
        return self.texto
    def publicada_recentemente(self):
        agora = timezone.now()
        passado_24hs = agora - datetime.timedelta(days=1)
        return passado_24hs <= self.data_publicacao <= agora
    publicada_recentemente.admin_order_field = 'data_publicacao'
    publicada_recentemente.boolean = True
    publicada_recentemente.short_description = 'É recente?'


###     Classe Opcao
##########################
class Opcao(models.Model):
    texto = models.CharField(max_length=100)
    quant_votos = models.IntegerField(default=0)
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)

    class Meta:
        ordering = ['texto']
        verbose_name = 'Opção'
        verbose_name_plural = 'Opções'
    def __str__(self):
        return self.texto

