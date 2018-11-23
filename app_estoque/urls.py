from django.urls import path

from . import views

urlpatterns = [
    #/estoque
    path('', views.index, name='index'),
    #/estoque/entrada
    path('entrada', views.entrada, name='entrada'),
    #/estoque/saida
    path('saida', views.saida, name='saida'),
    path('lista', views.lista, name='lista'),
    path('cadastro', views.cadastro, name='cadastro'),
    path('lista_compra', views.lista_compra, name='lista_compra'),
    #/estoque/estoque_detalhe/id
    path('estoque_detalhe/<int:id_produto>/', views.estoque_detalhe, name='estoque_detalhe'),

]
