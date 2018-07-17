from kivy.app import App
# kivy.require("1.8.0")
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.graphics import Line

from Controller.dbClass import TreinamentoDB
from Controller.moduleViCompGenerator import ModuleViCompGenerator
from Controller.perceptron import Perceptron

Window.size = (1280,720)

class Painter(Widget):
    def __init__(self,**kwargs):
        self.id = 'pincel'
        super(Painter, self).__init__(**kwargs)

    def on_touch_down(self, touch):
        with self.canvas:
            touch.ud["line"] = Line(points=(touch.x, touch.y),width=2)


    def on_touch_move(self, touch):
        touch.ud["line"].points += [touch.x, touch.y]
    def clearScreen(self):
        self.canvas.clear()

class Sobre(Screen):
    pass
class MainScreen(Screen):
    def start(self):
        self.manager.current = 'GerarAmostra'
    def Analisar(self):
        Window.size = (240, 360)
        self.manager.current = 'DesenhoAnalizar'

class GerarAmostra(Screen):
    def start(self):
        Window.size = (240, 360)
        self.manager.current = 'Desenho'
    def treinamento(self):
        app = App.get_running_app()
        # app.perceptron.gerarSinapses()
        app.perceptron.start()
        treino().open()
class AnalisarScreen(Screen):
    def print_screen(self):
        import glob
        arquivos = glob.glob('img/numero*')
        Window.screenshot(name=('img/numero.jpg'))
        numero = (len(arquivos))+1
        if(numero<10):
            name = "numero000" + str(numero)
        elif(numero>9) and (numero<100):
            name = "numero00" + str(numero)
        elif (numero > 99):
            name = "numero" + str(numero)
        app = App.get_running_app()
        app.vcGenerator = ModuleViCompGenerator()
        app.vcGenerator.readAndCreate(fileName=name)
        Window.size = (1280,720)
        pincel = self.buscaWidget('pincel')
        pincel.clearScreen()
        print(app.vcGenerator.vector)
        app = App.get_running_app()
        app.resultado= app.resultado + str(app.perceptron.reconhecimento(app.vcGenerator.vector))
        self.manager.current = 'Resultado'

    def buscaWidget(self, idSearch=""):  # busca widgets que nao estao inseridos em self.ids por serem novos
        children = self.children[:]
        while children:
            child = children.pop()
            children.extend(child.children)
            if child.id == str(idSearch):
                return child

class Resultado(Screen):
    def __init__(self,**kwargs):
        Clock.schedule_interval(self.updateScreen, 0.5)
        super(Resultado, self).__init__(**kwargs)
    def updateScreen(self,*args):
        app = App.get_running_app()
        self.ids.valorResultado.text= str(app.resultado)
    def acertei(self):
        app = App.get_running_app()
        app.resultado = 'O valor desenhado foi: '
        self.manager.current = 'main'
    def errei(self):
        app = App.get_running_app()
        app.resultado= 'O valor desenhado foi: '
        self.manager.current = 'InformarDado'
class InformarDado(Screen):
    def finalizar(self):
        app = App.get_running_app()
        bd = TreinamentoDB('bd/rna')
        dados=[(1,int(self.ids.valorReal.text),str(app.vcGenerator.vector))]
        bd.registraTreinamento(dados)
        # app.perceptron.start()
        app.perceptron.treinaNovo(app.vcGenerator.vector,int(self.ids.valorReal.text))
        self.manager.current = 'main'

class ScreenManagement(ScreenManager):
    pass

class treino(Popup):
    pass


class AnotherScreen(Screen):
    def print_screen(self):
        import glob
        arquivos = glob.glob('img/numero*')
        Window.screenshot(name=('img/numero.jpg'))
        numero = (len(arquivos))+1
        if(numero<10):
            name = "numero000" + str(numero)
        elif(numero>9) and (numero<100):
            name = "numero00" + str(numero)
        elif (numero > 99):
            name = "numero" + str(numero)
        app = App.get_running_app()
        app.vcGenerator = ModuleViCompGenerator()
        app.vcGenerator.readAndCreate(fileName=name)
        Window.size = (1280,720)
        pincel = self.buscaWidget('pincel')
        pincel.clearScreen()
        print(app.vcGenerator.vector)
        self.manager.current = 'InformarDado'

    def buscaWidget(self, idSearch=""):  # busca widgets que nao estao inseridos em self.ids por serem novos
        children = self.children[:]

        while children:
            child = children.pop()
            children.extend(child.children)
            if child.id == str(idSearch):
                return child

presentation = Builder.load_file("tela.kv")

class MainApp(App):

    def build(self):
        self.title= 'RNA Perceptron'
        self.dados=None
        self.perceptron = Perceptron()
        self.vcGenerator= None
        self.resultado= 'O valor desenhado foi: '
        return presentation


if __name__ == "__main__":
    MainApp().run()