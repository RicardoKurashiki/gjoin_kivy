# ---------- ACABO O TRABALHO --------------
# AGRADEÇO DE CORAÇÃO A PARTICIPAÇÃO DE TODOS
# ESPECIALMENTE DE CADU QUE CARREGO ESSE TRABALHOS NAS COSTAS


from kivy.config import Config
# Fixar tamanho
Config.set('graphics', 'resizable', False)
from kivy.lang.builder import Builder
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen, ScreenManager
import kivy.properties as kvProps
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.app import App
import sqlite3
import re
from DataBase_funcs import BancoDadosGrupos, BancoDadosMsg, BancoDadosRelacoes


# -------- CÓDIGO PRINCIPAL --------

regex = '^[a-z0-9]+[\._]?[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

def check(email):
    valid = True

    if(re.search(regex, email)):
        valid = True

    else:
        valid = False
        avisopop = 'Insira um e-mail valido.'

        pops = WarningPopup()
        pops.ids.aviso.text = avisopop
        pops.open()

    return valid

idLogado = 0 # Id será armazenado para acessar os grupos e informações relacionados a ele
idGrupoChat = 0
avisopop = ''

# -------- RECYCLE VIEW --------

class LinhaSearch(BoxLayout):
    nome_group = kvProps.StringProperty('')
    idGrupo = kvProps.NumericProperty()
    
    def clique(self):
        db = BancoDadosGrupos()
        GrupoList = db.listarGruposPorId(self.idGrupo)
        App.get_running_app().registro_atual = GrupoList
        App.get_running_app().route.transition.direction = 'left'
        App.get_running_app().route.current = 'entrar'

        global idGrupoChat
        idGrupoChat = self.idGrupo

        global nome_sala
        nome_sala = self.nome_group

class LinhaHomePage(BoxLayout):
    nome_group = kvProps.StringProperty('')
    idGrupo = kvProps.NumericProperty()

    def go_chat(self):
        db = BancoDadosGrupos()
        GrupoList = db.listarGruposPorId(self.idGrupo)
        App.get_running_app().registro_atual = GrupoList
        App.get_running_app().route.transition.direction = 'left'
        App.get_running_app().route.current = 'chat'

        global idGrupoChat
        idGrupoChat = self.idGrupo

class LinhaChat(BoxLayout):
    mensagem = kvProps.StringProperty('')

# -------- TELA LOGIN --------
class LoginPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # Logo do app
    imagem_app = kvProps.StringProperty('gjoinLogo.jpeg')

    def login(self):
        #Verificando se o login e senha estão correntos
        user = self.ids.log_email.text
        password = self.ids.log_pass.text
        conn = sqlite3.connect('BANCO.db')
        db = conn.cursor()
        db.execute('SELECT * FROM dados WHERE email = ? AND senha = ?', (user, password))

        if db.fetchall():
            #Chamando as variáveis globais para a função
            global idLogado

            # Mudança da tela de login para a home page
            self.manager.transition.direction = 'left'
            self.manager.current = 'home'

            # Armazenando o ID logado na variável global idLogado
            conn = sqlite3.connect('BANCO.db')
            db = conn.cursor()
            db.execute('''SELECT id FROM dados WHERE email = ? and senha = ?''', (user, password))
            idLogado = db.fetchone()[0]
            conn.close()

        else:
            global avisopop
            avisopop = 'O usuario e senha nao sao validos.'

            pops = WarningPopup()
            pops.ids.aviso.text = avisopop
            pops.open()

        conn.close()

    def go_register(self):
        self.manager.transition.direction = 'up'
        self.manager.current = 'register'

# -------- TELA REGISTRAR --------

class RegisterPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # Verifica e registra conta no banco de dados
    def register_account(self):
        global avisopop
        valid = True

        # Verificação de email no banco de dados
        conn = sqlite3.connect('BANCO.db')
        cursor = conn.cursor()
        cursor.execute("""SELECT email FROM dados;""")
        for registro in cursor.fetchall():
            if registro == (self.ids.reg_email.text,):
                valid = False
                print('Digite um email que não esteja em uso')
        conn.close()

        #Verifica se não há nenhum campo em branco
        if self.ids.reg_name.text == '':
            valid = False
            avisopop = 'Insira um nome.'

            pops = WarningPopup()
            pops.ids.aviso.text = avisopop
            pops.open()

        elif self.ids.reg_email.text == '':
            valid = False
            avisopop = 'Insira um e-mail.'

            pops = WarningPopup()
            pops.ids.aviso.text = avisopop
            pops.open()

        elif self.ids.reg_univ.text == '':
            valid = False
            avisopop = 'Insira uma Universidade.'

            pops = WarningPopup()
            pops.ids.aviso.text = avisopop
            pops.open()

        elif self.ids.reg_curso.text == '':
            valid = False
            avisopop = 'Insira um curso.'

            pops = WarningPopup()
            pops.ids.aviso.text = avisopop
            pops.open()

        elif self.ids.reg_pass.text == '':
            valid = False
            avisopop = 'Insira uma senha.'

            pops = WarningPopup()
            pops.ids.aviso.text = avisopop
            pops.open()

        elif self.ids.reg_confirmPass.text == '':
            valid = False
            avisopop = 'Insira uma confirmacao de senha.'

            pops = WarningPopup()
            pops.ids.aviso.text = avisopop
            pops.open()

        # Verifica se a confirmação de senha confere
        elif self.ids.reg_pass.text != self.ids.reg_confirmPass.text:
            valid = False
            avisopop = 'Senhas nao conferem.'

            pops = WarningPopup()
            pops.ids.aviso.text = avisopop
            pops.open()

        # Registra o cadastro no banco de dados caso passe por todas as verificações
        elif valid == True and check(self.ids.reg_email.text) == True:
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
            cursor.execute('''INSERT INTO dados (usuario, email, senha, universidade, curso) VALUES (?,?,?,?,?) ''',
                           (NovReg.nome, NovReg.email, NovReg.senha, NovReg.universidade, NovReg.curso))
            conn.commit()
            conn.close()

            avisopop = 'Registro realizado.'

            pops = WarningPopup()
            pops.ids.aviso.text = avisopop
            pops.open()


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
    imagem_app = kvProps.StringProperty('gjoinLogo.jpeg')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def go_to_chat(self): #Possivelmente: def go_to_chat(self, group)
        self.manager.transition.direction = 'left'
        self.manager.current = 'chat'

    def on_enter(self):
        global idLogado

        #Recycle View criando os botões do grupo
        db = BancoDadosRelacoes()
        grupos = db.listarGruposLogado(idLogado)
        self.ids.listagemhome.data = list()
        if grupos != None:
            for g in grupos:
                self.ids.listagemhome.data.append({'idGrupo': g.idGrupo, 'nome_group': g.nome_group})
        else:
            None

    def go_back(self):
        #Chama o idLogado para reiniciá-lo
        global idLogado
        idLogado = 0

        # Vai para página de login
        self.manager.transition.direction = 'right'
        self.manager.current = 'login'

    def go_to_create(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'create'
    
    def go_to_search(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'search'

# -------- TELA DE CHAT --------

class ChatPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def exit_chat(self):
        # Reinicia o id do chat que irá aparecer as mensagens
        global idGrupoChat
        idGrupoChat = None
        self.manager.transition.direction = 'right'
        self.manager.current = 'home'

    #Carrega as mensagens do chat aberto
    def load_message(self):
        db = BancoDadosMsg()
        mensagens = db.ReceberMensagem(idGrupoChat)
        self.ids.listagemchat.data = list()
        if mensagens != None:
            for m in mensagens:
                self.ids.listagemchat.data.append({'mensagem': m.mensagem})
        else:
            None

    # Carrega e envia uma nova mensagem pra aquele grupo específico
    def send_message(self):
        global idGrupoChat

        mensagem = self.ids.new_message.text
        db = BancoDadosMsg()

        db.EnviarMensagem(mensagem, idGrupoChat)
        mensagens = db.ReceberMensagem(idGrupoChat)
        self.ids.listagemchat.data = list()
        if mensagens != None:
            for m in mensagens:
                self.ids.listagemchat.data.append({'mensagem': m.mensagem})
        else:
            None
        
        self.ids.new_message.text = ''

# -------- CRIAR GRUPO --------

class CreatePage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def voltar(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'home'

    def criar_grupo(self):
        global avisopop
        global idLogado
        # ------ VARIAVEIS PARA A VERIFICAÇÃO -------
        self.nomeGrupo = self.ids.nome_novo_grupo.text
        self.faculGrupo = self.ids.faculdade_novo_grupo.text
        self.matGrupo = self.ids.materia_novo_grupo.text
        self.horGrupo = self.ids.horario_novo_grupo.text
        # Caso esteja tudo preenchido
        if (self.nomeGrupo and self.faculGrupo and self.matGrupo and self.horGrupo) != '':
            # Armazena as informações inseridas no banco de dados
            dbg = BancoDadosGrupos()
            dbg.criarNovoGrupo(self.nomeGrupo, self.faculGrupo, self.matGrupo, self.horGrupo, idLogado)
            
            dbr = BancoDadosRelacoes()
            dbr.NovaRelacao(idLogado)

            # Retorna para a home page
            self.manager.transition.direction = 'right'
            self.manager.current = 'home'

            # Zera os campos
            self.ids.nome_novo_grupo.text = ''
            self.ids.faculdade_novo_grupo.text = ''
            self.ids.materia_novo_grupo.text = ''
            self.ids.horario_novo_grupo.text = ''

        # Faltando nome para o grupo
        if self.nomeGrupo == '':
            avisopop = 'Informe um nome para o grupo.'

            pops = WarningPopup()
            pops.ids.aviso.text = avisopop
            pops.open()
        # Faltando faculdade para o grupo
        if self.faculGrupo == '':
            avisopop = 'Informe uma faculdade para o grupo'

            pops = WarningPopup()
            pops.ids.aviso.text = avisopop
            pops.open()
        # Faltando materia para o grupo
        if self.matGrupo == '':
            avisopop = 'Informe uma disciplina para o grupo'

            pops = WarningPopup()
            pops.ids.aviso.text = avisopop
            pops.open()
        # Faltando horario para o grupo
        if self.horGrupo == '':
            avisopop = 'Informe um horario para o grupo'

            pops = WarningPopup()
            pops.ids.aviso.text = avisopop
            pops.open()
        
# -------- PROCURAR GRUPO ---------

class SearchPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def returnhome(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'home'

    def TodosGrupos(self):
        self.pesquisa('')
    
    def pesquisa(self, nome):
        nome = self.ids.txBusca.text
        db = BancoDadosGrupos()
        grupos = db.listarGruposPorNome(nome)
        self.ids.listagem.data = list()
        if grupos != None:
            for g in grupos:
                self.ids.listagem.data.append({'idGrupo': g.idGrupo, 'nome_group': g.nome_group})       
        else:
            None

class JoinPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def load_message(self):
        global nome_sala
        self.ids.nome_da_sala.text = nome_sala

        global idGrupoChat

        db = BancoDadosMsg()
        mensagens = db.ReceberMensagem(idGrupoChat)
        self.ids.listagemchat.data = list()

        if mensagens != None:
            for m in mensagens:
                self.ids.listagemchat.data.append({'mensagem': m.mensagem})
        else:
            None

    def entrar_sim(self):
        global idLogado
        global idGrupoChat

        dbr = BancoDadosRelacoes()
        dbr.EntrarGrupo(idGrupoChat, idLogado)
        
        self.manager.transition.direction = 'right'
        self.manager.current = 'home'

    def entrar_nao(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'search'
    
# -------- POPUP DE AVISOS ---------

class WarningPopup(Popup):
    pass

# -------- CONSTRUINDO APP --------

class GjoinApp(App):
    def build(self):
        # Tamanho da tela
        Window.size = (400, 600)
        self.route = ScreenManager()
        # Rotas do aplicativo
        self.route.add_widget(LoginPage(name='login'))
        self.route.add_widget(RegisterPage(name='register'))
        self.route.add_widget(HomePage(name='home'))
        self.route.add_widget(ChatPage(name='chat'))
        self.route.add_widget(CreatePage(name='create'))
        self.route.add_widget(SearchPage(name= 'search'))
        self.route.add_widget(JoinPage(name= 'entrar'))
        # Nome do app
        self.title = 'GJoin - Aplicativo de Chat'
        return self.route

# -------- INICIANDO APP --------


GjoinApp().run()
