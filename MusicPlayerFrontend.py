import kivy
kivy.require("1.10.0")

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout

from kivy.core.window import Window

Window.clearcolor = (1, 1, 1, 1)

# Use mpb to access backend methods
import MusicPlayerBackend
mpb = MusicPlayerBackend.MusicPlayerBackend()

# Locating all the .kv files
from os import listdir
kv_path = "./kivyFiles/"
for kv in listdir(kv_path):
    print(kv)
    Builder.load_file(kv_path + kv)

class MainMenuScreen(Screen):
    pass

class MusicScreen(Screen):
    soundName = StringProperty()
    
    def playMusic(self):
        # At the moment it is hardcoded but later we will use
        # the fileChooser to choose the song
        mpb.soundFilePlay(mpb.soundFileLoader().get(0))
        self.soundNameChange(str(mpb.soundFileNameLoader().get(0)))
        print(self.soundName)        
    def pauseMusic(self):
        mpb.soundFilePause(mpb.soundFileLoader().get(0))
        
    def soundNameChange(self, name):
            # This function changes the label to the song
            # we are playing at that moment
        self.soundName = name
        

class FileChooserScreen(Screen):
    def selectFile(self, *args):
        try:
            self.label.text = args[1][0]
        except:
            pass
        
sm = ScreenManager()
sm.add_widget(MainMenuScreen(name = "main_menu"))
sm.add_widget(MusicScreen(name = "music"))
sm.add_widget(FileChooserScreen(name = "file_chooser"))

class MusicPlayerFrontendApp(App):
    def build(self):
        self.title = "Music Player"
        return sm
    
if __name__ == "__main__":
    MusicPlayerFrontendApp().run()

