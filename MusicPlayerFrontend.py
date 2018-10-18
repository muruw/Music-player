from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen

# Use mpb to access backend methods
import MusicPlayerBackend
mpb = MusicPlayerBackend.MusicPlayerBackend()

from os import listdir
kv_path = "./kivyFiles/"
for kv in listdir(kv_path):
    print(kv)
    Builder.load_file(kv_path + kv)

class MainMenuScreen(Screen):
    """
    display = ObjectProperty()
    
    def browseMusicFile(self):
        print("Valid faili")
        
    def playMusic(self):
        print("Muusika käib")
    """
    pass
class MusicScreen(Screen):
    def playMusic(self):
        mpb.soundFilePlay("ShortMusic.mp3")

sm = ScreenManager()
sm.add_widget(MainMenuScreen(name = "main_menu"))
sm.add_widget(MusicScreen(name = "music"))

class MusicPlayerFrontendApp(App):
    def build(self):
        self.title = "Music Player"
        return sm
    
if __name__ == "__main__":
    MusicPlayerFrontendApp().run()

