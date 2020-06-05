# -------- IMPORTAÇÕES --------
from kivy.config import Config
# Fixar tamanho
Config.set('graphics', 'resizable', False)
from kivy.lang.builder import Builder
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager
import kivy.properties as kvProps
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.app import App
import sqlite3
import re


# -------- CÓDIGO PRINCIPAL --------

regex = '^[a-z0-9]+[\._]?[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'


def check(email):
    conf = 1
    if(re.search(regex, email)):
        conf = 1
    else:
        print('Insira um e-mail válido')
        conf = 0
    return conf


lista = []
msg = []

isListaNew = False
# -------- TELA LOGIN --------


class LoginPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # Logo do app
    imagem_app = kvProps.StringProperty('gjoinLogo.png')

    def login(self):
        user = self.ids.log_email.text
        password = self.ids.log_pass.text
        conn = sqlite3.connect('BANCO.db')
        db = conn.cursor()
        db.execute(
            'SELECT * FROM dados WHERE email = ? AND senha = ?', (user, password))
        if db.fetchall():
            self.manager.transition.direction = 'left'
            self.manager.current = 'home'
        else:
            print('O usuário e senha não são válidos!')
        conn.close()

    def go_register(self):
        self.manager.transition.direction = 'up'
        self.manager.current = 'register'

# -------- TELA REGISTRAR --------


class RegisterPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # Empurra para o DB
    def register_account(self):
        conf = 1

        # Verificação de email no banco de dados
        conn = sqlite3.connect('BANCO.db')
        cursor = conn.cursor()
        cursor.execute("""SELECT email FROM dados;""")
        for registro in cursor.fetchall():
            if registro == (self.ids.reg_email.text,):
                conf = 0
                print('Digite um email que não esteja em uso')
        conn.close()

        if self.ids.reg_name.text == '':
            conf = 0
            print('Insira um nome')

        elif self.ids.reg_email.text == '':
            conf = 0
            print('Insira um email')

        elif self.ids.reg_univ.text == '':
            conf = 0
            print('Insira uma universidade')

        elif self.ids.reg_curso.text == '':
            conf = 0
            print('Insira um curso')

        elif self.ids.reg_pass.text == '':
            conf = 0
            print('Insira uma senha')

        elif self.ids.reg_confirmPass.text == '':
            conf = 0
            print('Insira uma confirmação de senha')

        elif self.ids.reg_pass.text != self.ids.reg_confirmPass.text:
            conf = 0
            print('Senha não confere')

        elif conf == 1 and check(self.ids.reg_email.text) == 1:
            class Registro(object):
                def __init__(self, nome, email, universidade, curso, senha, confsenha):
                    self.nome = nome
                    self.email = email
                    self.universidade = universidade
                    self.curso = curso
                    self.senha = senha
                    self.confsenha = confsenha

            NovReg = Registro(nome=self.ids.reg_name.text, email=self.ids.reg_email.text, universidade=self.ids.reg_univ.text,
                              curso=self.ids.reg_curso.text, senha=self.ids.reg_pass.text, confsenha=self.ids.reg_confirmPass.text)  # Criação do novo registro
            conn = sqlite3.connect('BANCO.db')  # Conexão com o DB
            cursor = conn.cursor()

            cursor.execute("""INSERT INTO dados (usuario, email, senha, universidade, curso) VALUES (?,?,?,?,?) """,
                           (NovReg.nome, NovReg.email, NovReg.senha, NovReg.universidade, NovReg.curso))

            conn.commit()
            print(
                '------------------------------------  Registrado ------------------------------------')
            conn.close()

            self.manager.transition.direction = 'down'
            self.manager.current = 'login'

            self.ids.reg_name.text = ''
            self.ids.reg_email.text = ''
            self.ids.reg_univ.text = ''
            self.ids.reg_curso.text = ''
            self.ids.reg_pass.text = ''
            self.ids.reg_confirmPass.text = ''

    def cancel_register(self):
        self.manager.transition.direction = 'down'
        self.manager.current = 'login'

# -------- TELA PRINCIPAL --------


class HomePage(Screen):
    # Logo do app
    imagem_app = kvProps.StringProperty('gjoinLogo.png')

    # Lupa
    Lupa = kvProps.StringProperty('lupa.png')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def go_to_chat(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'chat'

    def on_enter(self):
        global isListaNew
        # Caso a lista de grupos esteja vazia, não aparece nenhum botão nem da erro
        if len(lista) >= 1:
            if isListaNew == True:
                # Cria o botão para entrar no chat (Não sei pra que serve o lambda, mas ele faz funcionar então safe)
                self.ids.listview.add_widget(Button(
                    text=lista[-1], on_release=lambda x: self.go_to_chat(), font_size=30, size_hint_y=None, height=50))
                isListaNew = False

    def go_back(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'login'

    def go_to_create(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'create'


# -------- TELA DE CHAT --------


class ChatPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def exit_chat(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'home'

    def send_message(self):
        # Transforma o texto da caixa de msg em variavel 'message'
        message = self.ids.new_message.text
        # Limpa a caixa de texto
        self.ids.new_message.text = ''
        # Faz basicamente a mesma função de criar grupo.
        if message:
            msg.append(f'> {message}')
            self.ids.chat_de_texto.add_widget(
                Label(text=msg[-1], font_size=20, size_hint_y=None, height=30))


# -------- CRIAR GRUPO --------


class CreatePage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def voltar(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'home'

    def criar_grupo(self):
        # TODO -> Criar um novo db para cada grupo
        # Não sei se tem como, mas criar um banco de dados gerais para todos os grupos
        # E dentro desse BD criar um banco de dados mais especificos com cada especificação
        # (NOME, CURSO, HORA, sla)
        global isListaNew
        # A lista tem que ser substituida pelo banco de dados
        # ------ VARIAVEIS PARA A VERIFICAÇÃO -------
        self.nomeGrupo = self.ids.nome_novo_grupo.text
        self.faculGrupo = self.ids.faculdade_novo_grupo.text
        self.matGrupo = self.ids.materia_novo_grupo.text
        self.horGrupo = self.ids.horario_novo_grupo.text
        # Caso esteja tudo preenchido
        if(self.nomeGrupo and self.faculGrupo and self.matGrupo and self.horGrupo) != '':
            lista.append(self.nomeGrupo)
            # Evitar criar grupo acidentalmente
            isListaNew = True
            self.ids.nome_novo_grupo.text = ''
            self.ids.faculdade_novo_grupo.text = ''
            self.ids.materia_novo_grupo.text = ''
            self.ids.horario_novo_grupo.text = ''
            self.manager.transition.direction = 'right'
            self.manager.current = 'home'
        # Faltando nome para o grupo
        if self.nomeGrupo == '':
            print('Informe um nome para o grupo')
        # Faltando faculdade para o grupo
        if self.faculGrupo == '':
            print('Informe uma faculdade para o grupo')
        # Faltando materia para o grupo
        if self.matGrupo == '':
            print('Informe uma matéria para o grupo')
        # Faltando horario para o grupo
        if self.horGrupo == '':
            print('Informe um horário para o grupo')

# -------- CONSTRUINDO APP --------


class GjoinApp(App):
    def build(self):
        # Tamanho da tela
        Window.size = (400, 600)
        route = ScreenManager()
        # Rotas do aplicativo
        route.add_widget(LoginPage(name='login'))
        route.add_widget(RegisterPage(name='register'))
        route.add_widget(HomePage(name='home'))
        route.add_widget(ChatPage(name='chat'))
        route.add_widget(CreatePage(name='create'))
        # Nome do app
        self.title = 'GJoin - Aplicativo de Chat'
        return route

# -------- INICIANDO APP --------


GjoinApp().run()
