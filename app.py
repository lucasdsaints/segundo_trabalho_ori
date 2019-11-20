# Segundo trabalho de Organização e Recuperação da Informação 2019-02
# Alunos: Caliton Junior e Lucas Santos
# Professor: Wendel Melo

import sys
import nltk
from math import log, sqrt

def main():
    # gera indice
    nome_arq_bases = sys.argv[1]
    arq_bases = open(nome_arq_bases, "r")
    lista_bases = arq_bases.read().split("\n")
    arq_bases.close()

    indice_invertido = gera_indice_invertido(lista_bases)
    
    # gera e grava tabela de ponderação
    tabela_poderacao = gera_tabela_ponderacao(lista_bases, indice_invertido)
    gravar_tabela_ponderacao(lista_bases, tabela_poderacao)

    # trata a consulta
    nome_arq_consulta = sys.argv[2]
    consulta = open(nome_arq_consulta, "r").read()
    consulta = gera_ponderacao_pesquisa(consulta, len(lista_bases), indice_invertido)
    
    # similaridade e resultado
    similaridade = calcula_similaridade(tabela_poderacao, consulta, list(indice_invertido.keys()))
    grava_resuldado(similaridade, lista_bases)

def grava_resuldado(similaridade, lista_bases):
    similaridade = sorted(similaridade.items(), key=lambda x: x[1], reverse=True)
    n_resultados = 0
    texto = ""
    for doc in similaridade:
        if doc[1] != 0:
            n_resultados += 1
            texto += f"{lista_bases[doc[0] -1]} - {doc[1]:.4f}\n"
    arq_resultado = open("resposta.txt", "w")
    arq_resultado.write(f"{n_resultados}\n{texto}")
    arq_resultado.close()

def calcula_similaridade(bases, consulta, termos_da_base):
    n_base = 0
    similaridade = {}
    for base in bases:
        somatorio1 = 0
        somatorio2 = 0
        somatorio3 = 0
        n_base += 1
        for termo in termos_da_base:
            if termo in bases[base] and termo in consulta:
               somatorio1 += bases[base][termo] * consulta[termo]
            if termo in bases[base]:
                somatorio2 += bases[base][termo]**2
            if termo in consulta:
                somatorio3 += consulta[termo]**2
        similaridade[n_base] = 0 if ((sqrt(somatorio2) * sqrt(somatorio3)) == 0) else somatorio1 / (sqrt(somatorio2) * sqrt(somatorio3))
    return similaridade

def gera_ponderacao_pesquisa (consulta, n_docs, indice_invertido):
    consulta = limpar_texto(consulta)
    consulta = extrair_radicais(consulta)

    ponderacao = {}
    for termo in consulta:
        if termo in indice_invertido:
            tf = 1 + log(consulta.count(termo), 10)
            idf = log(n_docs/len(indice_invertido[termo]))
            ponderacao[termo] = tf * idf
        else:
            ponderacao[termo] = 0
    return ponderacao

def gera_tabela_ponderacao (lista_bases, indice_invertido):
    tabela_poderacao = {}
    doc = 0
    n_docs = len(lista_bases)
    for base in lista_bases:
        doc += 1
        texto = open(base, "r").read()
        vetor_palavras = limpar_texto(texto)
        vetor_radicais = extrair_radicais(vetor_palavras)

        ponderacao_doc = {}
        for radical in vetor_radicais:
            freq_rad_doc = indice_invertido[radical][doc]

            tf = 1 + log(freq_rad_doc, 10)
            idf = log(n_docs/len(indice_invertido[radical]), 10)

            ponderacao_doc[radical] = tf * idf
        
        tabela_poderacao[doc] = ponderacao_doc
    return tabela_poderacao

def gravar_tabela_ponderacao (lista_bases, tabela_poderacao):
    arq_ponderacao = open("pesos.txt", "w")
    n_doc = 0
    for doc in lista_bases:
        n_doc += 1
        texto = doc + ": "
        for termo in tabela_poderacao[n_doc]:
            texto += f"{termo},{tabela_poderacao[n_doc][termo]:.4f}   "
        texto += "\n"
        arq_ponderacao.write(texto)
    arq_ponderacao.close()

def gera_indice_invertido (lista_bases):
    # gerar indice
    i = 0
    indice_invertido = {}
    for base in lista_bases:
        i += 1
        texto = open(base, "r").read()
        vetor_palavras = limpar_texto(texto)
        vetor_radicais = extrair_radicais(vetor_palavras)

        for radical in vetor_radicais:
            if radical not in indice_invertido:
                indice_invertido[radical] = {i:1}
            else:
                if i in indice_invertido[radical]:
                    indice_invertido[radical][i] = indice_invertido[radical][i] + 1
                else:
                    indice_invertido[radical][i] = 1
    
    # gravar indice em arquivo
    # arq_indice = open("indice.txt", "w")

    # for radical in indice_invertido:
    #     string = '' + radical + ': '
    #     for base in indice_invertido[radical]:
    #         string += '{base},{qtd} '.format(base=base, qtd=indice_invertido[radical][base])
    #     string += '\n'
    #     arq_indice.write(string)

    # arq_indice.close()

    # retorno do indice
    return indice_invertido

def limpar_texto (str):
    str = str.lower()
    str =  str.replace("\n", " ")
    str = str.replace(',', " ")
    str = str.replace('...', " ")
    str = str.replace('.', " ")
    str = str.replace('!', " ")
    str = str.replace('?', " ")
    str = str.replace('&', " ")
    vetor_palavras = ' '.join(str.split()).split(' ')
    stopwords = nltk.corpus.stopwords.words('portuguese')
    vetor_palavras_limpo = []
    for palavra in vetor_palavras:
        if palavra not in stopwords:
            vetor_palavras_limpo.append(palavra)

    return vetor_palavras_limpo

def extrair_radicais (objeto):
	stemmer = nltk.stem.RSLPStemmer()

	# se o objeto for só uma palavra
	if (type(objeto) == type('string')):
		return stemmer.stem(objeto)
	# se o objeto for um conjunto de palavras
	else:
		vetor_radicais = []
		for palavra in objeto:
			vetor_radicais.append(stemmer.stem(palavra))

	return vetor_radicais

main()