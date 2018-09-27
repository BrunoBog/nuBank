import configparser
import json
from datetime import datetime
from pynubank import Nubank
from src.model.Compra import Despesa
from flask import Flask, render_template

app = Flask(__name__)
config = configparser.ConfigParser()
config.read_file(open('config.ini'))
nu = Nubank(config['DEFAULT']['usuario'], config['DEFAULT']['senha']) # subistituir por usu e senha
dia_fechamento = int(config['DEFAULT']['dia_do_fechamento'])


def add_desp(n):
    return Despesa(
        descricao=n['description'],
        categoria=n['category'],
        valor=n['amount'],
        data=datetime.strptime(n['time'], "%Y-%m-%dT%H:%M:%SZ"),
        titulo=n['title'],
        detalhes=n['details'], #json.dumps(n['details'])
        id=n['id'],
        _links=n['_links'],
        link=n['href'],
    )


def grava_saida(resultado, arquivosaida):
    arquivo = open(arquivosaida, "w")
    arquivo.writelines(resultado)
    arquivo.close()


def busca_valores_atuais():
    # Lista de dicionários contendo todos os eventos do  Nubank (Compras, aumento de limite, pagamentos,etc)
    transactions = nu.get_account_statements()
    despesas = {}
    i = 0
    for n in transactions:
        data_despesa = datetime.strptime(n['time'], "%Y-%m-%dT%H:%M:%SZ")
        # if hoje is None else hoje
        hoje = datetime.now()

        # Após o fechamento do mês anterior
        if data_despesa.year == hoje.year and data_despesa.month == hoje.month - 1 and data_despesa.day > dia_fechamento:
            despesas.update({i: add_desp(n).json()})

        # Despesas do mês corrente
        if data_despesa.year == hoje.year and data_despesa.month == hoje.month and data_despesa.day <= dia_fechamento:
            despesas.update({i: add_desp(n).json()})

        # no caso do mês de dezembro...
        if data_despesa.year == hoje.year - 1 and data_despesa.month == 12 and data_despesa.day > dia_fechamento:
            despesas.update({i: add_desp(n).json()})

        i = i + 1
    return despesas


def categoriza_valores(despesas):
    if despesas is None:
        return
    categorias = dict()
    for key, val in despesas.items():
        if len(val['detalhes']) > 1:
            if 'tags' in json.loads(val['detalhes']).keys():
                for n in json.loads(val['detalhes'])['tags']:
                    if n not in categorias.keys():
                        categorias.update({n: val['valor']})
                    else:
                        categorias.update({n: val['valor'] + categorias[n]})
                    if n == r'r\u00e9veillon':
                        print(val['valor'])

    return categorias

@app.route("/")
def lista_opções():
    return "/listarComprasAtuais <br> /listarCategorizado <br> /teste"

@app.route("/listarComprasAtuais")
def lista_valores_atuais():
    return json.dumps(busca_valores_atuais())


@app.route("/busca<mes><ano><diafechamento>")
def busca_compras():
    pass

@app.route('/listarCategorizado')
def lista_valores_categorizados():
    despesas = busca_valores_atuais()
    return json.dumps(categoriza_valores(despesas=despesas))

@app.route("/teste")
def teste():
    lista = busca_valores_atuais()
    # testando saida em jSon
    grava_saida(json.dumps(lista), 'C:\\Users\\BOG\Desktop\\saida.json')

    soma = 0
    for n in lista.values():
        soma += int(n['valor'])
        print(n['data'], n['descricao'], n['valor'])
    print("total = " + str(soma/100))

    return "total = " + str(soma/100)


if __name__ == '__main__':
    app.run(debug=True)

