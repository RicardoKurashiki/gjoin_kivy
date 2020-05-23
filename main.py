from kivy.config import Config
# Fixar tamanho
Config.set('graphics', 'resizable', False)

from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.app import App


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
        pass
    
    def cancel_register(self):
        self.manager.transition.direction = 'down'
        self.manager.current = 'login'

class HomePage(Screen):
        # Logo do app
    imagem_app = StringProperty('gjoinLogo.png')
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
