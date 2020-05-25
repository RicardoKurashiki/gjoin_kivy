from kivy.config import Config
# Fixar tamanho
Config.set('graphics', 'resizable', False)

from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.app import App
import sqlite3
import re

regex = '^[a-z0-9]+[\._]?[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
def check(email):  
    conf = 1
    if(re.search(regex,email)):  
        conf = 1
    else:  
        print('Insira um e-mail válido')
        conf = 0
    return conf

class LoginPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # Logo do app
    imagem_app = StringProperty('gjoinLogo.png')

    # TODO: Criar a funcionalidade de checar no DB a conta
    def login(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'home'

    def go_register(self):
        self.manager.transition.direction = 'up'
        self.manager.current = 'register'


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

        elif self.ids.reg_confirmPass.text ==  '':
            conf = 0
            print('Insira uma confirmação de senha')

        elif self.ids.reg_pass.text != self.ids.reg_confirmPass.text:
            conf = 0
            print('As senhas digitadas precisam ser iguais!')
        
        elif conf == 1 and check(self.ids.reg_email.text) == 1:
            class Registro(object):
                def __init__(self, nome, email, universidade, curso, senha, confsenha):
                    self.nome = nome
                    self.email = email
                    self.universidade = universidade
                    self.curso = curso
                    self.senha = senha
                    self.confsenha = confsenha

            NovReg = Registro(nome = self.ids.reg_name.text, email = self.ids.reg_email.text, universidade = self.ids.reg_univ.text, curso = self.ids.reg_curso.text, senha = self.ids.reg_pass.text, confsenha = self.ids.reg_confirmPass.text) # Criação do novo registro
            conn = sqlite3.connect('BANCO.db') # Conexão com o DB
            cursor = conn.cursor()

            cursor.execute("""INSERT INTO dados (usuario, email, senha, universidade, curso) VALUES (?,?,?,?,?) """, (NovReg.nome, NovReg.email, NovReg.senha, NovReg.universidade, NovReg.curso))

            conn.commit()
            print('------------------------------------  Registrado ------------------------------------')
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

class HomePage(Screen):
        # Logo do app
    imagem_app = StringProperty('gjoinLogo.png')

    # Lupa
    Lupa = StringProperty('lupa.png')
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def go_back(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'login'
    
    def go_to_chat(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'chat'

class ChatPage(Screen):
    def exit_chat(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'home'

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
        # Nome do app
        self.title = 'GJoin - Aplicativo de Chat'
        return route

GjoinApp().run()
