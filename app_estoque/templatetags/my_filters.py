# meus filtros customizados
from django import template
from django.template.defaultfilters import register

#register = template.library()


@register.filter(name='dicKey')
def dicKey(dict, chave):
    return dict[chave][0]
dicKey = register.filter('dicKey', dicKey)

def dicKey1(dict, chave):
    return dict[chave][1]
dicKey1 = register.filter('dicKey1', dicKey1)
