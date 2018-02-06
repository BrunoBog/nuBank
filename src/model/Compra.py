import json


class Despesa(object):

    def __init__(self, descricao, categoria, valor, data, titulo, detalhes, id, _links, link):
        self.descricao = descricao
        self.categoria = categoria
        self.valor = valor
        self.data = data
        self.titulo = titulo
        self.detalhes = detalhes
        self.id = id
        self._links = _links
        self.link = link


    def json(self):
        return {
            "descricao": self.descricao,
            "categoria": self.categoria,
            "valor": self.valor,
            "data": str(self.data),
            "titulo": self.titulo,
            "detalhes": json.dumps(self.detalhes),
            "id": self.id,
            "_links": self._links,
            "link": self.link
        }

