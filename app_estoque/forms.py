from django import forms


# nao esta sendo utilizado
#it hasnt been used
class EntradaForm(forms.Form):
    produto = forms.CharField(label='item_produto',max_length=100)
    qtd = forms.IntegerField(label='quantidade')
