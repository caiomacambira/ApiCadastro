import json
import sqlite3

from flask import Flask, request
        

from dao import UsuarioDao
from models import Usuario

app = Flask(__name__)

@app.route('/add_user', methods=['POST'])
def add_user():
    nome = request.json['nome']
    senha = request.json['senha']
    email = request.json['email']
    telefone = request.json['telefone']

    novo_usuario = Usuario(nome, senha, email, telefone)
    usuario_dao = UsuarioDao(sqlite3.connect('bd.sqlite3'))
    novo_usuario = usuario_dao.adicionar(novo_usuario)
    return json.dumps(novo_usuario, default=vars)

@app.route('/users')
def users ():
    usuario_dao = UsuarioDao(sqlite3.connect('bd.sqlite3'))
    lista_usuarios = usuario_dao.listar()
    return json.dumps(lista_usuarios, default=vars)
    


@app.route('/users/<int:id>')
def consultar_user(id):
    usuario_dao = UsuarioDao(sqlite3.connect('bd.sqlite3'))
    consulta_usuario = usuario_dao.consultar_user(id)
    if consulta_usuario:
        return json.dumps(consulta_usuario, default=vars)
    else:
        return 'Não existe usuário com este id'


@app.route('/edit_user/<int:id>', methods=['PATCH'])
def edit_user(id):
    nome = request.json['nome']
    email = request.json['email']
    telefone = request.json['telefone']
    user_to_be_updated = Usuario(nome=nome, email=email, senha=None, telefone=telefone, id=id)
    user_dao = UsuarioDao(sqlite3.connect('bd.sqlite3'))
    user_to_be_updated = user_dao.atualizar(user_to_be_updated)
    return json.dumps(user_to_be_updated, default=vars)


@app.route('/delete_user/<int:id>', methods=['DELETE'])
def delete_user(id):
    usuario_dao = UsuarioDao(sqlite3.connect('bd.sqlite3'))
    usuario_dao.deletar(id)
    return f'Usuário de id "{id}" foi deletado com sucesso!' 
    
