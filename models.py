import json


class Usuario:
    def __init__(self, nome,senha,email, telefone, id=None):
        self.id = id
        self.nome = nome
        self.senha = senha
        self.email = email
        self.telefone = telefone

