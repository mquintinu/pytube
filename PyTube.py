# Interface Gráfica
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.animation import Animation
# para alterar a cor de fundo
import re
import os
# para baixar do Youtube
from pytube import YouTube
# Variáveis
_linkInvalido = False
_qualidade = ""
diretorio = ""

# Definir as janelas
class Tela_Principal(Screen):
    
    kv_link = ObjectProperty(None)
    kv_path = ObjectProperty(None)
    kv_btnDown = ObjectProperty(None)   
    kv_label = ObjectProperty(None) 
    kv_SelecionaDiretorio = ObjectProperty(None)    
    

    def btnDownload_click(self, widget, *args):
        # variáveis
        _link = self.ids.kv_link.text
        _diretorio = self.ids.kv_path.text  
        _mp3 = self.ids.switch_mp3.active        
                        
        if (_link and _diretorio) != '':  
            if (_mp3):
                BaixaSomenteMP3(self, _link, _diretorio, widget, *args)                        
            else:
                BaixaVideo(self, _link, _diretorio, widget, *args)                                              

    def Switch_Click(self, switchObject, switchValue):
        if (switchValue):
            _mp3 = True # baixa somente o MP3
        else:
            _mp3 = False # baixa o video inteiro

    def Slider_Qualidade(self, *args): 
        global _qualidade  
        if int(args[1]) == 1:            
            self.slider_text.text = "Qualidade: Padrão"
        elif int(args[1]) == 2:
            self.slider_text.text = "Qualidade: Alta"   
            _qualidade = "HD"         
                   
    ## Volta texto do botão
    def VoltaBotao(self):
        self.ids.kv_btnDown.text = "Download!"    
        self.ids.kv_btnDown.disabled = False 
    
    def Atualiza(self):
        self.ids.kv_path.text = diretorio

class Tela_Diretorio(Screen):    
    def Path_Selecionado(self, path):
        global diretorio
        diretorio = path 

class WindowManager(ScreenManager):
    pass

# Define qual será o arquivo .kv do "front-end"
kv = Builder.load_file("PyTube.kv")   

def BaixaSomenteMP3(self, _link, _diretorio, widget, *args):

    try: 
        # Baixa o vídeo        
        yt = YouTube(_link)
        yt.streams.get_audio_only().download(_diretorio)        
    
        ## Altera a extensão do arquivo de .MP4 para .MP3    
        for file in os.listdir(_diretorio):
            if re.search('mp4', file):                
                arquivo_divido = os.path.splitext(file)
                arq_mp3 = arquivo_divido[0] + '.mp3'            
                
                arq_mp4 = os.path.join(_diretorio,file)
                arq_mp3 = os.path.join(_diretorio,arq_mp3)

                for fileMP3 in os.listdir(_diretorio):
                    if re.search('mp3', fileMP3):
                        arquivoMP3_divido = os.path.splitext(fileMP3)
                        if arquivoMP3_divido[0] + '.mp3' == arquivo_divido[0] + '.mp3':
                            RemoveArq_mp3 = os.path.join(_diretorio,fileMP3)
                            os.remove(RemoveArq_mp3) 
                            os.rename(arq_mp4,arq_mp3)
                            self.kv_btnDown.text = "Download completo!"
                            FazAnimacao_Botao(self, widget, *args)
                            return
                    
                os.rename(arq_mp4,arq_mp3)
                self.kv_btnDown.text = "Download completo!"
                FazAnimacao_Botao(self, widget, *args)   
    except:
        self.ids.kv_btnDown.text = "Link ou diretório inválido"
        self.ids.kv_btnDown.disabled = True

def BaixaVideo(self, _link, _diretorio, widget, *args):
    global _qualidade  
       
    try:        
        yt = YouTube(_link)
        if _qualidade == "HD":            
            yt.streams.get_highest_resolution().download(_diretorio) # baixa em HD
            
        else:
            yt.streams.first().download(_diretorio) # baixa na primeira qualidade que encontrar
        
        self.kv_btnDown.text = "Download completo!" 
        FazAnimacao_Botao(self, widget, *args)                           
    except:                
        self.ids.kv_btnDown.text = "Link ou diretório inválido"
        self.ids.kv_btnDown.disabled = True

def FazAnimacao_Botao(self, widget, *args):
    # aumenta o botão
    animacao = Animation(size_hint=(0.6, .4), duration = 1)
    # volta ao tamanho normal
    animacao += Animation(size_hint=(0.5, .3), duration = 1)        

    animacao.start(widget)    

class MyLayout(Widget):
    pass

class MinhaApp(App):
    def build(self):
        return kv

if __name__ == '__main__':
    MinhaApp().run()       
