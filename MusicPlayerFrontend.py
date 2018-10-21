from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.boxlayout import BoxLayout

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
    def playMusic(self):
        mpb.soundFilePlay("ShortMusic.mp3")

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

