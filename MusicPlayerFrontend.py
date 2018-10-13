# Kivy imports
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

import MusicPlayerBackend

class TestScreen(GridLayout):
    def __init__(self, **kwargs):
        super(TestScreen, self).__init__(**kwargs)
        
        self.cols = 2
        self.row = 2
        
        self.buttonSoundPlay = Button(text = "Play music")
        self.buttonSoundPlay.bind(on_press = self.playSound)
        self.add_widget(self.buttonSoundPlay)
        
    def playSound(self, instance):
        print("Played a sound!")
        mpb.soundFilePlay("SampleMusic.wma")

# Kivy requires writing App after the class name
class MusicPlayerApp(App):
    def build(self):
        return TestScreen()
        

""" Use mpb to access backend methods"""
mpb = MusicPlayerBackend.MusicPlayerBackend()

""" MusicPlayer().run() käivitab programmi"""
if __name__ == "__main__":
    MusicPlayerApp().run()
