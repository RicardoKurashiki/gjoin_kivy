import sqlite3

class Grupo:
    def __init__(self, idGrupo, nome_group, faculdade, materia, horario, idUser):
        self.idGrupo = idGrupo
        self.nome_group = nome_group
        self.faculdade = faculdade
        self.materia = materia
        self.horario = horario
        self.idUser = idUser

class User:
    def __init__(self, id, usuario, email, senha, universidade, curso):
        self.id = id
        self.usuario = usuario
        self.email = email
        self.senha = senha
        self.universidade = universidade
        self.curso = curso

class BancoDadosGrupos:
    def listarGruposPorNome(self, parteNome):
        conn = sqlite3.connect('BANCO.db')
        cursor = conn.cursor()

        cursor.execute('''
        SELECT * FROM groupsdb
        WHERE nome LIKE '%{}%'
        '''.format(parteNome)
        )

        result = list()

        for registro in cursor.fetchall():
            result.append(Grupo(registro[0], registro[1], registro[2], registro[3], registro[4], registro[5]))
        conn.close()
        if result != []:
            return result
        else: 
            return None

    def listarGruposPorId(self, id):
        conn = sqlite3.connect('BANCO.db')
        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM groupsdb
        WHERE idGrupo = {}
        """.format(id)
        )

        registro = cursor.fetchone()
        conn.close()
        if registro != None:
            return Grupo(registro[0], registro[1], registro[2], registro[3], registro[4], registro[5])
        else: 
            return None
    
    def listarGruposLogado(self, idLogado):

        conn = sqlite3.connect('BANCO.db')
        cursor = conn.cursor()

        cursor.execute('''
        SELECT * FROM groupsdb
        WHERE idUser = {}
        '''.format(idLogado)
        )
        
        result = list()

        for registro in cursor.fetchall():
            result.append(Grupo(registro[0], registro[1], registro[2], registro[3], registro[4], registro[5]))
        conn.close()
        if result != []:
            return result
        else: 
            return None