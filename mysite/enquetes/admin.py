from django.contrib import admin
from .models import Pergunta, Opcao, Rotulo, Autor, Perfil

admin.AdminSite.site_header = 'Administração da Aplicação de Enquetes'

### Definição do Formulário para as Perguntas
#############################################
class OpcaoInline(admin.TabularInline):
    model = Opcao
    extra = 2

class PerguntaAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['autor', 'texto', 'rotulos']}),
        ('Informações de Data', {'fields': ['data_publicacao', 'data_encerramento']})
    ]
    inlines = [OpcaoInline]
    list_display = ('texto', 'id', 'autor', 'data_publicacao', 'publicada_recentemente')
    list_filter = ['data_publicacao']
    search_fields = ['texto']

admin.site.register(Pergunta, PerguntaAdmin)


### Definição do Formulário para os Rótulos
###########################################
class RotuloAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'id')

admin.site.register(Rotulo, RotuloAdmin)


### Definição do Formulário para os Autores
###########################################
class PerfilInline(admin.StackedInline):
    model = Perfil

class AutorAdmin(admin.ModelAdmin):
    inlines = [PerfilInline]
    list_display = ('nome', 'id')

admin.site.register(Autor, AutorAdmin)


