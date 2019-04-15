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

def getFromLink(html):
    """
    Funcao que pega o conteudo de uma ancora. 

    Nao eh possivel apenas usar a funcao trim pois cada ancora tem a referencia dentro da propria tag.
    """
    text = html.lower().split("<a ")[1]
    start = text.find('>') + 1
    end = text.find('<')

    return text[start:end]

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
    #encontra o ID de cada uma das linhas da tabela;
    td_tag = '<span class="txt_arial_8pt_gray">'
    #cada linha da tabela tem 2 entradas com a tag td_tag, entao pegamos somente a primeira
    IDs = [trim(ROW, td_tag)[0] for ROW in rows]
    return IDs

def isDivided(HTML):
    """
    Faz uma busca pelo HTML da pagina, procurando uma tabela que indique que as disciplinas foram divididas

    Essa eh a unica tabela cuja tag eh escrita com letras minusculas, e eh alinhado no centro
    """
    table_tag = '<table align="center">'
    #se essa tag for encontrada, find retorna a posicao em que ela ocorre
    #se a tag nao existe, retorna -1
    return HTML.find(table_tag) > -1

def getSubjectDivisions(HTML):
    """
    Faz uma busca pelo HTML da pagina, para encontrar subdivisoes das materias. 

    Por exemplo, na primeira pagina, tem 5 separacoes: [A-D], [E-F], [G-N], [O-R] e [S-W]
    """
    #a lista de divisoes eh uma tabela que possui apenas uma linha
    table_tag = '<table align="center">'
    print(HTML[HTML.find('<table a'):HTML.find('<table a')+50])
    tables = trim(HTML, table_tag)
    return tables


def getSubjects(HTML):
    """
    Passa pelo HTML pegando todos os nomes e codigos de disciplinas

    A tabela de disciplinas tem todas as tags escritas com letras maiusculas
    """
    #pega as linhas da unica tabela presente na pagina
    table_tag = '<TABLE align="center">'
    tables = trim(HTML, table_tag)
    rows = trim(tables[0], "<TR>")

    #Pega o primeiro e o segundo valor da linha
    td_tag = '<span class="txt_arial_8pt_gray">'
    subjects = [trim(ROW, td_tag)[0:2] for ROW in rows]
    #o segundo valor da lista em subjects eh uma ancora, precisamos extrair o texto dela
    for sub in subjects:
        #como listas sempre apontam para a mesma regiao de memoria, alterando sub, alteramos a lista dentro de subjects tambem
        sub[1] = getFromLink(sub[1])
    return subjects

base_url = 'https://uspdigital.usp.br/jupiterweb/'
start_url = 'jupColegiadoLista?'
type_url = 'tipo=D'
subject_url = 'jupDisciplinaLista?codcg='#inserir o ID de cada instituicao + '&' no final da URL

#actual spidering done like this, under is just debugging
pagina = req.get(base_url + start_url + type_url)
if(pagina.status_code != 200):
    print(pagina.status_code)
else:
    #lista todas as urls a serem requisitadas em busca de materias
    #subject_url_list = [base_url + subject_url + str(ID) + '&' + type_url for ID in getUniversitySchools(pagina.text)]
    subject_url_list = [base_url +subject_url + '58&' + type_url]
    count = 0
    for URL in subject_url_list:
        #print(URL)
        count += 1
        pagina = req.get(URL)
        if(not pagina.ok):
            continue
        #algumas paginas tem as disciplinas separadas por range de letras. 
        #primeiro precisamos descobrir se a pagina tem essa subdivisao
        if(isDivided(pagina.text)):
            div = getSubjectDivisions(pagina.text)
            print(div)
        else:
            subjects = getSubjects(pagina.text)
            for sub in subjects:
                print(sub)
        break
