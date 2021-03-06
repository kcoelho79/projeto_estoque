from django.db import models
from django.utils import timezone

class Produto(models.Model):
    data_cad = models.DateTimeField(auto_now_add='True')
    item_text = models.CharField(max_length=200, unique=True)
    item_descricao = models.TextField(blank=True )
    min_estoque = models.IntegerField(default=0)


    def __str__(self):
        return self.item_text


class Estoque(models.Model):
    SITUACAO = (
        ('Entrada', 'entrada'),
        ('Saida', 'saida'),
    )

    data_timestamp = models.DateTimeField(auto_now_add='True')
    data = models.DateTimeField(default=timezone.now)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    situacao = models.CharField(max_length=7, choices=SITUACAO)
    qtd = models.IntegerField(default=0)

    def __str__(self):
        return "%s qtd %i de %s" %(self.data, self.qtd, self.produto.item_text)
