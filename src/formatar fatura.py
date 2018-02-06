import os
import sys


def ler_arquivo(path):
    if not os.path.exists(path):
        print("arquivo {} nao existe".format(path))
        return None
    else:
        _file = open(path, "r")
        conteudo = _file.readlines()
        _file.close()
        return conteudo


def read_meta_data(diretorio):
    data = open(diretorio,"r")
    meta_data=[]
    for line in data:
        line_data = line.split('\t')
        meta_data.append((line_data[0],line_data[1],line_data[2]))
    data.close()
    return meta_data


def grava_saida(resultado, arquivoSaida):
    if not os.path.exists(arquivoSaida):
        print("arquivo {} nao existe, foi criado agora".format(arquivoSaida))

    arquivo = open(arquivoSaida, "w")
    for item in resultado:
            arquivo.writelines(item + "\n")
    arquivo.close()


def lista_conteudo(diretorio):
    todos_arquivos = os.listdir(diretorio)


caminho_do_arquivo = r"C:\Users\bruno.alves\OneDrive\Workspace\Phyton\UtilitariosPython\NUBank\src"
nome_arquivo = "\gastos.txt"
data = ler_arquivo(caminho_do_arquivo+nome_arquivo)

if data is None:
    sys.exit(-1)

cont = 0
resultado = []
linha = ""
for x in data:
    linha += " " + x[:len(x) - 1] + "\t"
    cont += 1
    if cont == 3:
        resultado.append(linha)
        cont =0
        linha = ""


grava_saida(resultado, caminho_do_arquivo + "saida.txt")





