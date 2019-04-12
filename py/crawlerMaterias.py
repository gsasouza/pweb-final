#! /usr/bin/python3

import requests as req

def genDelimiter(tag):
    """
    Funcao que, dada uma tag de HTML, retorna os delimitadores de abertura e fechamento da tag, para usar na funcao trim
    """
    #a string passada eh a tag que contem a informacao desejada
    #copiada exatamente
    open_tag = tag

    #a tag de termino eh bem menor, pois nao tem as informacoes do css
    #primeiro encontramos onde a tag termina e o css inicia
    close_tag = tag[:tag.find(' ')]  + '>'
    #agora adicionamos o marcador de fim de tag
    close_tag = '</' + close_tag[1:]
    return open_tag,close_tag

def trim(html, tag):
    """
    Funcao que retorna os conteudos de todos os blocos abertos por tag
    """
    open_tag, close_tag = genDelimiter(tag)

    #separa todas as ocorrencias de open_tag
    trimmed = html.split(open_tag)
    #joga fora a primeira ocorrencia, pois ocorre antes da primeira ocorrencia de open_tag
    trimmed = trimmed[1:]
    #joga fora o que vem depois de close_tag e caracteres em branco no comeco ou final, para todos os elementos da lista
    trimmed = [s[: s.find(close_tag)].strip() for s in trimmed]

    #joga fora todas as linhas vazias
    trimmed = [s for s in trimmed if s is not '']

    return trimmed

def getLink(html):
    """
    Funcao que encontra o link em uma ancora
    """
    #encontra a primeira ancora e joga fora tudo que vem antes dela, incluindo o comeco da tag
    link = html.lower().split("<a ")[1]

    link = link[link.find('href="') + len('href="'):]
    link = link[:link.find('"')]

    return link

def getUniversitySchools(HTML):
    """
    Passa pelo HTML pegando todos os links para pesquisa de materias por instituicao

    Existem 2 tabelas que contem as informacoes, ambas estao na tag abaixo, e sao as unicas com essa tag em especifico
    """
    table_tag = '<table border="0" align="center" width="500" >'
    #encontra as tabelas com as instituicoes
    tables = trim(HTML, table_tag)
    #pega as linhas da tabela
    rows = trim(tables[0], "<tr>") + trim(tables[1],"<tr>")
    #encontra o link de cada linha das tabelas
    links = [getLink(s) for s in rows]
    return links


start_url = 'https://uspdigital.usp.br/jupiterweb/jupColegiadoLista?tipo=D'

#actual spidering done like this, under is just debugging
#pagina = req.get(start_url)
#if(pagina.status_code != 200):
#    print(pagina.text)
#else:
#    tag = '<li>'
#    for item in getUniversitySchools(pagina.text):
#        print(item)

#debug spidering
with open("1.html") as f:
    s = f.read()
for line in getUniversitySchools(s):
    print(line)
