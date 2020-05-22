from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.app import App


class LoginPage(Screen):
    # Logo do app
    imagem_app = StringProperty('gjoinLogo.png')
    
    def go_register(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'register'

class RegisterPage(Screen):

    def register_account(self):
        pass
    
    def cancel_register(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'login'

class GjoinApp(App):
    def build(self):
        # Tamanho da tela
        Window.size = (400, 600)
        # Cor de fundo
        Window.clearcolor = (0.5, 0.5, 0.5, 0.5)
        route = ScreenManager()
        # Rotas do aplicativo
        route.add_widget(LoginPage(name='login'))
        route.add_widget(RegisterPage(name='register'))
        # Nome do app
        self.title = 'GJoin - Aplicativo de Chat'
        return route

GjoinApp().run()
