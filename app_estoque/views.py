from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.db.models import Q, Sum
from .forms import EntradaForm
from .models import Produto,Estoque
from django.urls import reverse
import datetime

def index(request):
    return render(request, 'index.html')

def lista_compra(request):
    produtos = Produto.objects.all()
    return render(request, 'lista_compra.html', {'produtos':produtos})

#lista estoque (ALTERAR)
def lista(request):
    produtos = Produto.objects.all()
    return render(request, 'lista.html', {'produtos':produtos})


def estoque_detalhe(request, id_produto=None):

    if request.method == 'POST':
    # recebe os dados do formulario
        item = request.POST.get('f_item')
        data_inicial = request.POST.get('f_data_inicial')
        data_final = request.POST.get('f_data_final')
        # iniciar validacao dos campos de filtro data
        if data_inicial:
            ano_ini,mes_ini,dia_ini = data_inicial.split(',')
            data_inicial_limpa= datetime.date(int(ano_ini),int(mes_ini),int(dia_ini))
            estoque = get_list_or_404(Estoque, produto__id=int(item), data__date=data_inicial_limpa)
            # se data inicial e final recebeu data nao vazio
            if data_final:
                ano_final,mes_final,dia_final = data_final.split(',')
                data_final_limpa= datetime.date(int(ano_final),int(mes_final),int(dia_final))
                estoque = get_list_or_404(Estoque, produto__id=int(item), data__date__range=(data_inicial_limpa, data_final_limpa))
        # filtro data esta vazio
        else:
            estoque = get_list_or_404(Estoque, produto__id=int(item))
        total = Estoque.objects.filter(produto=int(item)).aggregate(Sum('qtd'))
    else:
        estoque = get_list_or_404(Estoque, produto__id=id_produto)
        total = Estoque.objects.filter(produto=id_produto).aggregate(Sum('qtd'))
    # variavel TOTAL resultado da soma de todos ent e saida do produto
    # Sum (biblioteca) faz a Soma e retorar um DIC campo__sum
    return render(request, 'estoque_detalhe.html', {'estoque':estoque, 'total':total['qtd__sum']})

def cadastro(request):
    mensagem=""
    try:
        if request.method == 'POST':
            produto = Produto(item_text=request.POST['nome_produto'],item_descricao=request.POST['descricao_produto'],min_estoque=request.POST['min_estoque'],total_estoque=request.POST['total_estoque'])
            produto.save()
            mensagem="Gravado com Sucesso"

    except Exception as e:
            mensagem="ERROR NO CADASTRO"
    except ValueError as e:
            mensagem="FUDEU"

    return render(request, 'cadastro.html', {'mensagem':mensagem})

# sugestao transformar as duas views de entrada e saida em estoque_detalhe
# para deixar o codigo mais limpo e evitar repeticao
def saida(request):
    produtos = Produto.objects.all()
    status=""
    if request.method == 'POST':
    # lqtd e litens sao LIsta que recebem dados formulario, criadas
    # para facilitar
        lqtd = request.POST.getlist('f_qtd')
        litens = request.POST.getlist('item')
    # pega o tamanho da interaçao (qtos itens teve atualizacao no estoque)
    # para gerar loop e gravar as atualizacoes no baco
        tamanho=len(litens)
        for pos in range(tamanho):
    # no form os itens (produto) que nao serao atualizado, receberam '0' de qtd
    # isso e necessario para que as listas de itens e qtd tenha o mesmo tamanho,
    # para quando for buscar as posicao do vetor,
    # entao para o item que tem 0 não sera gravado no banco
            if not lqtd[pos] == '0':
                produto = Produto.objects.get(id=litens[pos])
                produto.estoque_set.create(qtd=-int(lqtd[pos]),situacao='saida')
                produto.total_estoque= produto.total_estoque - int(lqtd[pos])
                produto.save()
            else:
                continue

        return HttpResponseRedirect(reverse('saida'))
    else:
        return render(request, 'saida.html', {'produtos':produtos, 'status':status, 't_views':"saida"})

def entrada(request):
    produtos = Produto.objects.all()
    status=""
    if request.method == 'POST':
    # lqtd e litens sao LIsta que recebem dados formulario, criadas
    # para facilitar
        lqtd = request.POST.getlist('f_qtd')
        litens = request.POST.getlist('item')
    # pega o tamanho da interaçao (qtos itens teve atualizacao no estoque)
    # para gerar loop e gravar as atualizacoes no baco
        tamanho=len(litens)
        for pos in range(tamanho):
    # no form os itens (produto) que nao serao atualizado, receberam '0' de qtd
    # isso e necessario para que as listas de itens e qtd tenha o mesmo tamanho,
    # para quando for buscar as posicao do vetor,
    # entao para o item que tem 0 não sera gravado no banco
            if not lqtd[pos] == '0':
                produto = Produto.objects.get(id=litens[pos])
                produto.estoque_set.create(qtd=int(lqtd[pos]),situacao='entrada')
                produto.total_estoque= produto.total_estoque + int(lqtd[pos])
                produto.save()
            else:
                continue

        return HttpResponseRedirect(reverse('entrada'))
    else:
        return render(request, 'entrada.html', {'produtos':produtos, 'status':status, 't_views':"entrada"})
