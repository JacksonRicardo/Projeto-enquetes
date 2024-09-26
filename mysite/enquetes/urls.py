
from django.urls import path
from . import views

app_name = 'enquetes'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path(
        'adiciona/', views.AdicionaEnqueteView.as_view(),
        name='adiciona_enquete'
    ),
    path(
        'autor/novo', views.AdicionaAutorView.as_view(),
        name='adiciona_autor'
    ),
    path(
        'pergunta/<int:id>/', views.DetalhesView.as_view(),
        name='detalhes'
    ),
    path(
        'pergunta/<int:id>/votacao/', views.VotacaoView.as_view(),
        name='votacao'
    ),
    path(
        'pergunta/<int:id>/resultado/', views.ResultadoView.as_view(),
        name='resultado'
    ),
]