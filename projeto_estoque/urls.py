"""projeto_estoque URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from app_estoque import views


urlpatterns = [

# para sistema com multiplos APP e recomendado uma url por APP,
# no caso deve usar um include conforme exemplo abaixo
    #path('estoque/', include('app_estoque.urls')),
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
    path('admin/', admin.site.urls),
    path('signup/', views.signup, name='signup'),
#    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('allauth.urls')),

]
