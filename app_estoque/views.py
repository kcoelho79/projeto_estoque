from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.db.models import Q, Sum
from .forms import EntradaForm
from .models import Produto,Estoque
from django.urls import reverse
import datetime
from datetime import date
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    count = User.objects.count()
    return render(request, 'index.html', {
        'count': count
    })

@login_required
def lista(request, compra=None):
    produtos = Produto.objects.all()
    dic_produtos = {}
    for item in produtos:
        estoque = Estoque.objects.filter(produto__id = item.id)
        produto = item.item_text #nome do produto
        total = sum([ i.qtd for i in estoque])
        minimo = item.min_estoque
        comprar = minimo - total
        dic_produtos.update({item.item_text: (total,comprar)})
    if compra == "True":
        return render(request, 'lista_compra.html', {'dic_produtos':dic_produtos, 'produtos':produtos})
    return render(request, 'lista.html', {'dic_produtos':dic_produtos, 'produtos':produtos})

@login_required
def remover(request, item, pag_saida=None): #recebe o id do item
    item_estoque = get_object_or_404(Estoque, id=item)
    qtd_item= item_estoque.qtd
    produto = item_estoque.produto_id # Antes de apagar pega o ID do produto
    operacao = item_estoque.situacao # pera a operacao de entrada ou saida
    item_estoque.delete()
    estoque = Estoque.objects.filter(produto_id=produto)
    if pag_saida == operacao:
        return HttpResponseRedirect(reverse('estoque', args=(operacao,)), {'estoque':estoque})

    return HttpResponseRedirect(reverse('estoque_detalhe', args=(produto,)), {'estoque':estoque})

@login_required
def remover_produto(request, id_produto):
    produto_remover = Produto.objects.get(id=id_produto)
    #mensagem = "o produto %s foi removido" %(produto_remover.item_text)
    produto_remover.delete()
    produtos = Produto.objects.all()
    return HttpResponseRedirect(reverse('lista'))
    #return render(request, 'alerta.html' , {'mensagem':mensagem})
 
@login_required
def estoque_detalhe(request, id_produto=None):

    if request.method == 'POST':
    # recebe os dados do formulario
        item = request.POST.get('f_item')
        data_inicial = request.POST.get('f_data_inicial')
        data_final = request.POST.get('f_data_final')
        # iniciar validacao dos campos de filtro data
        if data_inicial:
            dia_ini,mes_ini,ano_ini = data_inicial.split('/')
            data_inicial_limpa= datetime.date(int(ano_ini),int(mes_ini),int(dia_ini))
            #estoque = get_list_or_404(Estoque, produto__id=int(item), data__date=data_inicial_limpa)
            # gte= maior ou igual
            estoque = Estoque.objects.filter(produto__id=int(item)).filter(data__date__gte=data_inicial_limpa)
            # se data inicial e final recebeu data nao vazio
            if data_final:
                dia_final,mes_final,ano_final = data_final.split('/')
                data_final_limpa= datetime.date(int(ano_final),int(mes_final),int(dia_final))
                estoque = Estoque.objects.filter(produto__id=int(item)).filter(data__date__range=(data_inicial_limpa, data_final_limpa))

        # filtro data esta vazio
        else:
            estoque = get_list_or_404(Estoque, produto__id=int(item))

    else:
        if id_produto == 0: 
            estoque = Estoque.objects.all()
        else: 
            estoque = Estoque.objects.filter(produto__id=id_produto)
        
    # usando o sum para somar uma lista de valores que recebe do obj estoque
    total = sum([ i.qtd for i in estoque])
    # variavel TOTAL resultado da soma de todos ent e saida do produto
    # Sum (biblioteca) faz a Soma e retorar um DIC campo__sum
    produtos = Produto.objects.all() # levar todos os itens de produto, para preencher o select box codigo
    return render(request, 'estoque_detalhe.html', {'estoque':estoque, 'total':total, 'produtos':produtos})

@login_required
def cadastro(request, id_produto=None):
    mensagem=""

    if request.method == 'POST':
        Nome_produto = request.POST.get('f_nome_produto')
        Item_descricao = request.POST.get('f_descricao_produto')
        Min_estoque = request.POST.get('f_min_estoque')
        # verifica se o post e sobre cadastrar novo prodtuo ou alterar produto
        if id_produto:
            mensagem="produto ALTERADO com sucesso"
            edicao="True"
            Produto.objects.filter(id=id_produto).update(item_text=Nome_produto,item_descricao=Item_descricao,min_estoque=Min_estoque)
            produto_edicao = Produto.objects.get(id=id_produto)

        else:
            mensagem="produto CADASTRADO com sucesso"
            edicao="False"
            produto = Produto(item_text=Nome_produto,item_descricao=Item_descricao,min_estoque=Min_estoque)
            produto.save()
            produto_edicao= None

    else: # nao e o metodo POST
        if id_produto:
            mensagem="Modo edicao"
            edicao="True"
            produto_edicao = Produto.objects.get(pk=id_produto)

        else:
            mensagem="Modo de Cadastro"
            edicao="False"
            produto_edicao = None

    return render(request, 'cadastro.html', {'produto':produto_edicao, 'edicao':edicao, 'mensagem':mensagem})

@login_required
def estoque(request, operacao=None):
    # operacao = operacao de entrada (soma) ou saida (subtrai) do estoque
    produtos = Produto.objects.all()
    if request.method == 'POST':
        lqtd = request.POST.getlist('f_qtd')
        litens = request.POST.getlist('item')
        ldata = request.POST.get('data')

    # pega o tamanho da interaçao (qtos itens teve atualizacao no estoque)
    # para gerar loop e gravar as atualizacoes no baco
        tamanho=len(litens)
        for pos in range(tamanho):
    # no form os itens (produto) que nao serao atualizado, receberam '0' de qtd
    # isso e necessario para que as listas de itens e qtd tenha o mesmo tamanho,
    # para quando for buscar as posicao do vetor,
    # entao para o item que tem 0 não sera gravado no banco
            if not lqtd[pos] == '0':
                if operacao =="saida":
                    lqtd[pos] = -1 * int(lqtd[pos])
                produto = Produto.objects.get(id=litens[pos])
                produto.estoque_set.create(qtd=(lqtd[pos]),situacao=operacao,data=ldata)
                produto.save()
            else:
                continue

        return HttpResponseRedirect(reverse('estoque', args=(operacao,)), {'operacao':operacao})
    else:
        #date.__date= para formatar a buscar por um objeto datetime ao invez string
        latest = Estoque.objects.filter(situacao=operacao, data_timestamp__date=date.today()).order_by('-data')[:5]
        return render(request, 'estoque.html', {'produtos':produtos, 'operacao':operacao, 'latest':latest})


def signup(request):
    # usando function form 
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {
        'form': form
    })

