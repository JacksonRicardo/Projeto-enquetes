from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from .models import Pergunta, Opcao, Autor
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class AdicionaAutorView(generic.View):
    def get(self, request, *args, **kwargs):
        # preparar a exibição do forumlário de cadastramento
        return render(request, 'enquetes/novo_autor.html')

    def post(self, request, *args, **kwargs):
        # recuperação dos dados enviados pelo formulário
        try:
            nome = request.POST['first_name']
            sobrenome = request.POST['last_name']
            email = request.POST['email']
            login = request.POST['login']
            senha1 = request.POST['senha1']
            senha2 = request.POST['senha2']
            if nome and sobrenome and email and login and senha1 and senha2:
                if not senha1 == senha2:
                    messages.error(request,'Senhas informadas não são iguais!')
                    return render(request, 'enquetes/novo_autor.html')
                # criação e persistência das instâncias
                user = User.objects.create_user(login, email, senha1)
                user.first_name = nome
                user.last_name = sobrenome
                user.save()
                nome_completo = '{} {}'.format(nome, sobrenome)
                autor = Autor(nome=nome_completo, user=user)
                autor.save()
                messages.success(request, 'Novo autor: {}, salvo com sucesso'.format(nome))
            else:
                messages.error(
                    request,
                    'Todos os campos são obrigatórios. Tente novamente!'
                )
                return render(request, 'enquetes/novo_autor.html')
        except KeyError:
            messages.error(
                request,
                'Parâmetros necessários não informados. Tente novamente!'
            )
            return render(request, 'enquetes/novo_autor.html')
        # o encaminhamento para a página de cadastramento de nova enquete
        return HttpResponseRedirect(reverse('enquetes:index'))


@method_decorator(login_required, name='dispatch')
class AdicionaEnqueteView(generic.View):
    def get(self, request, *args, **kwargs):
        # preparar a exibição do forumlário de cadastramento
        return render(request, 'enquetes/nova_enquete.html')

    def post(self, request, *args, **kwargs):
        # recuperação dos dados enviados pelo formulário
        try:
            texto = request.POST['texto']
            encerramento = request.POST['encerramento']
            op1 = request.POST['op1']
            op2 = request.POST['op2']
            op3 = request.POST['op3']
            op4 = request.POST['op4']
            op5 = request.POST['op5']
            op6 = request.POST['op6']
            if texto and encerramento and op1 and op2:
                # criação e persistência das instâncias
                publicacao = timezone.now()
                pergunta = Pergunta(
                    texto = texto,
                    data_publicacao = publicacao,
                    data_encerramento = encerramento,
                    autor = request.user.autor
                )
                pergunta.save()
                op1 = Opcao(texto=op1, pergunta=pergunta)
                op1.save()
                op2 = Opcao(texto=op2, pergunta=pergunta)
                op2.save()
                messages.success(request, 'Enquete cadastrada com sucesso.')
                if op3:
                    op = Opcao(texto=op3, pergunta=pergunta)
                    op.save()
                if op4:
                    op = Opcao(texto=op4, pergunta=pergunta)
                    op.save()
                if op5:
                    op = Opcao(texto=op5, pergunta=pergunta)
                    op.save()
                if op6:
                    op = Opcao(texto=op6, pergunta=pergunta)
                    op.save()
            else:
                messages.error(
                    request,
                    'Informe ao menos o texto, a data de encerramento e duas opções!'
                )
                return render(request, 'enquetes/nova_enquete.html')
        except KeyError:
            messages.error(
                request,
                'Parâmetros necessários não enviados, tente novamente!'
            )
            return render(request, 'enquetes/nova_enquete.html')
        # o encaminhamento para a página inicial da aplicação
        return HttpResponseRedirect(reverse('enquetes:index'))

class IndexView(generic.View):
    def get(self, request, *args, **kwargs):
        lista_perguntas = Pergunta.objects.filter(
            data_publicacao__lte = timezone.now()
        ).filter(
            data_encerramento__gte = timezone.now()
        ).order_by('data_encerramento')
        contexto = { 'lista_perguntas': lista_perguntas,}
        return render(request, 'enquetes/index.html', contexto)

class DetalhesView(generic.View):
    def get(self, request, *args, **kwargs):
        id = self.kwargs['id']
        # pergunta = get_object_or_404(Pergunta, pk=id)
        pergunta = None
        try:
            pergunta = Pergunta.objects.filter(
                data_publicacao__lte = timezone.now()
            ).get(pk = id)
        except Pergunta.DoesNotExist:
            raise Http404("Identificador de enquete inválido!")
        contexto = { 'pergunta': pergunta, }
        return render(request, 'enquetes/detalhes.html', contexto)

class ResultadoView(generic.View):
    def get(self, request, *args, **kwargs):
        id = self.kwargs['id']
        pergunta = get_object_or_404(Pergunta, pk=id)
        contexto = { 'pergunta': pergunta, }
        return render(request, 'enquetes/resultado.html', contexto)

class VotacaoView(generic.View):
    def post(self, request, *args, **kwargs):
        id = self.kwargs['id']
        pergunta = get_object_or_404(Pergunta, pk=id)
        try:
            selecionada = pergunta.opcao_set.get(pk=request.POST['id_opcao'])
        except (KeyError, Opcao.DoesNotExist):
            contexto = {
                'pergunta': pergunta,
                'error_message': "Selecione uma opção váliada",
            }
            return render(request, 'enquetes/detalhes.html', contexto)
        else:
            selecionada.quant_votos += 1
            selecionada.save()
            return HttpResponseRedirect(
                reverse('enquetes:resultado', args=(pergunta.id,))
            )

"""
------------------------------------------------------------------------------
----   Outras formas alternativas de representação de elementos de view  -----
------------------------------------------------------------------------------

### INDEX - alternativa 1: função de view
#########################################
def index(request):
    lista_perguntas = Pergunta.objects.order_by('-data_publicacao')[:5]
    contexto = { 'lista_perguntas': lista_perguntas,}
    return render(request, 'enquetes/index.html', contexto)

### INDEX - alternativa 2: extendendo a classe ListView
#######################################################
class IndexView(generic.ListView):
    template_name = 'enquetes/index.html'
    context_object_name = 'lista_perguntas'
    def get_queryset(self):
        return Pergunta.objects.order_by('-data_publicacao')[:5]

### DETALHES - alternativa 1: função de view
############################################
def detalhes(request, id_pergunta):
    pergunta = get_object_or_404(Pergunta, pk=id_pergunta)
    contexto = { 'pergunta': pergunta, }
    return render(request, 'enquetes/detalhes.html', contexto)

### DETALHES - alternativa 2: extendendo a classe DetailView
############################################################
class DetalhesView(generic.DetailView):
    model = Pergunta
    template_name = 'enquetes/detalhes.html'

### RESULTADO - alternativa 1: função de view
#############################################
def resultado(request, id_pergunta):
    pergunta = get_object_or_404(Pergunta, pk=id_pergunta)
    contexto = { 'pergunta': pergunta, }
    return render(request, 'enquetes/resultado.html', contexto)

### RESULTADO - alternativa 2: extendendo a classe DetailView
#############################################################
class ResultadoView(generic.DetailView):
    model = Pergunta
    template_name = 'enquetes/resultado.html'

### VOTACAO: na forma de uma função de view
###########################################
def votacao(request, id_pergunta):
    pergunta = get_object_or_404(Pergunta, pk=id_pergunta)
    try:
        selecionada = pergunta.opcao_set.get(pk=request.POST['id_opcao'])
    except (KeyError, Opcao.DoesNotExist):
        contexto = {
            'pergunta': pergunta, 'error_message': "Selecione uma opção váliada",
        }
        return render(request, 'enquetes/detalhes.html', contexto)
    else:
        selecionada.quant_votos += 1
        selecionada.save()
        return HttpResponseRedirect(
            reverse('enquetes:resultado', args=(pergunta.id,))
        )
"""