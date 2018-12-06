from django.urls import path

from . import views

urlpatterns = [
    #/estoque
    path('', views.index, name='index'),
    #/estoque/entrada  ou /estoque/saida
    path('estoque/<operacao>/', views.estoque, name='estoque'),
    path('lista', views.lista, name='lista'),
    #/estoque/cadastro/edicao=true or false/id
    path('cadastro/', views.cadastro, name='cadastro'),
    path('cadastro/<int:id_produto>/', views.cadastro, name='cadastro_edicao'),
    path('lista/<compra>/', views.lista, name='lista_compra'),
    #/estoque/estoque_detalhe/id
    path('estoque_detalhe/<int:id_produto>/', views.estoque_detalhe, name='estoque_detalhe'),
    path('remover/<int:item>/<pag_saida>', views.remover, name='remover'),
    path('remover_produto/<int:id_produto>/', views.remover_produto, name='remover_produto'),


]
