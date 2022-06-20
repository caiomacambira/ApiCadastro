
from models import Usuario

SQL_CRIA_TABELA_USUARIO = """
        create table if not exists usuario(
        id integer primary key autoincrement,
        nome text not null,
        senha text not null,
        telefone text not null,
        email text UNIQUE not null
    )"""

SQL_LISTA_USUARIOS = 'select id,nome,senha,telefone,email from usuario'

SQL_CRIA_USUARIO = 'insert into usuario(nome, senha, telefone,email) values (?,?,?,?)'
#so
SQL_CONSULTA_USUARIO_POR_ID = 'SELECT id, nome, telefone, email from usuario where id = ?'

SQL_ATUALIZAR_USUARIO = 'update usuario set nome=?, email=?, telefone=? where id = ?'

SQL_DELETAR_USUARIO = 'delete from usuario where id = ?'

class UsuarioDao:
    def __init__(self, db):
        self.__db = db
        cursor = self.__db.cursor()
        cursor.execute(SQL_CRIA_TABELA_USUARIO)

    def listar(self):
        cursor = self.__db.cursor()
        cursor.execute(SQL_LISTA_USUARIOS)
        usuarios = self.converter_para_usuarios(cursor.fetchall())
        return usuarios

    def converter_para_usuarios(self,usuarios):
        def cria_usuario_tupla(tupla):
            return Usuario(nome=tupla[1], senha=tupla[2], telefone=tupla[3], email=tupla[4], id=tupla[0])
        return list(map(cria_usuario_tupla, usuarios))

    def adicionar(self,usuario):
        cursor =self.__db.cursor()
        tupla_usuario = (usuario.nome, usuario.senha, usuario.telefone, usuario.email)
        cursor.execute(SQL_CRIA_USUARIO,tupla_usuario)
        self.__db.commit()
        return usuario

    def atualizar(self, usuario):
        cursor = self.__db.cursor()
        tupla_edit_usuario = (usuario.nome, usuario.email, usuario.telefone, usuario.id)
        cursor.execute(SQL_ATUALIZAR_USUARIO, tupla_edit_usuario)
        self.__db.commit()
        return usuario

    def consultar_user(self, id):
        cursor = self.__db.cursor()
        cursor.execute(SQL_CONSULTA_USUARIO_POR_ID, (id,)) 
        dados = cursor.fetchone()
        # usuario = self.converter_para_usuarios(dados) if dados else None
        #  id, nome, telefone, email
        usuario = None
        if(dados):
            usuario = Usuario(nome=dados[1], senha=None, email=dados[2], telefone=dados[3], id=dados[0])
        return usuario

    def deletar(self, id):
        cursor = self.__db.cursor()
        cursor.execute(SQL_DELETAR_USUARIO, (id,)) 
        self.__db.commit()
        return True

