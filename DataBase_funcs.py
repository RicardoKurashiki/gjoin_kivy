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

class Message:
    def __init__(self, idMsg, idGrupo, mensagem):
        self.idMsg = idMsg
        self.idGrupo = idGrupo
        self.mensagem = mensagem

# Manipulação do banco de dados dos grupos
class BancoDadosGrupos:
    def criarNovoGrupo(self, nome, faculdade, materia, horario, idUser):
        conn = sqlite3.connect('BANCO.db')
        cursor = conn.cursor()

        cursor.execute('''
        INSERT INTO groupsdb(idGrupo, nome, faculdade, materia, horario, idUser)
        VALUES (NULL,?,?,?,?,?)
        ''', (nome, faculdade, materia, horario, idUser)
        )
        conn.commit()
        conn.close()

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

class BancoDadosMsg:
    def EnviarMensagem(self, mensagem, idGrupo):
        conn = sqlite3.connect('BANCO.db')
        cursor = conn.cursor()

        cursor.execute('''
        INSERT INTO msgdb(idMsg, idGrupo, mensagem)
        VALUES (NULL,?,?)
        ''', (idGrupo, mensagem)
        )
        conn.commit()
        conn.close()
    
    def ReceberMensagem(self, idGrupo):
        conn = sqlite3.connect('BANCO.db')
        cursor = conn.cursor()

        cursor.execute('''
        SELECT * FROM msgdb
        WHERE idGrupo = {}
        '''.format(idGrupo)
        )
        
        result = list()

        for registro in cursor.fetchall():
            result.append(Message(registro[0], registro[1], registro[2]))

        conn.close()

        if result != []:
            return result
        else: 
            return None

class BancoDadosRelacoes:
    def NovaRelacao(self, idLogado):
                
        conn = sqlite3.connect('BANCO.db')
        cursor = conn.cursor()

        cursor.execute('''
        SELECT idGrupo FROM groupsdb WHERE idUser = {}
        ORDER BY idGrupo DESC'''.format(idLogado)
        )

        idGrupoCriado = cursor.fetchone()[0]

        conn.close()

        conn = sqlite3.connect('BANCO.db')
        cursor = conn.cursor()

        cursor.execute('''
        INSERT INTO relacoesdb(idGrupo, idUser)
        VALUES (?, ?)''', (idGrupoCriado, idLogado)
        )
        conn.commit()
        conn.close()

    def listarGruposLogado(self, idLogado):

        conn = sqlite3.connect('BANCO.db')
        cursor = conn.cursor()

        cursor.execute('''
        SELECT idGrupo FROM relacoesdb
        WHERE idUser = {}
        '''.format(idLogado)
        )
        
        ids = []

        for registro in cursor.fetchall():
            ids.append(registro[0])

        conn.close()

        result = list()

        for i in ids:
            conn = sqlite3.connect('BANCO.db')
            cursor = conn.cursor()

            cursor.execute('''
            SELECT * FROM groupsdb
            WHERE idGrupo = {}
            '''.format(i)
            )

            for registro in cursor.fetchall():
                result.append(Grupo(registro[0], registro[1], registro[2], registro[3], registro[4], registro[5]))
                conn.close()

        if result != []:
            return result
        else: 
            return None
    
    def EntrarGrupo(self, idGrupo, idLogado):

        conn = sqlite3.connect('BANCO.db')
        cursor = conn.cursor()

        cursor.execute('''
        INSERT INTO relacoesdb(idGrupo, idUser)
        VALUES (?, ?)''', (idGrupo, idLogado)
        )

        conn.commit()
        conn.close()
            


