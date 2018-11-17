import kivy
import MusicPlayerBackend

# Use mpb to access backend methods
mpb = MusicPlayerBackend.MusicPlayerBackend()
db = MusicPlayerBackend.Database()

kivy.require("1.10.0")

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty
from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.core.window import Window

Window.clearcolor = (1, 1, 1, 1)

# Locating all the .kv files
from os import listdir

kv_path = "./kivyFiles/"
for kv in listdir(kv_path):
    print(kv)
    Builder.load_file(kv_path + kv)

# We will initialize the database
db.DatabaseSetup()
print("LVO: " + str(db.ListViewObjects()))


class MainMenuScreen(Screen):
    pass


class MusicScreen(Screen):

    sound_names_list = []
    soundDirectory = db.ListViewObjects()
    for sound_name in soundDirectory.items():
        sound_names_list.append(sound_name[1])

    soundName = StringProperty()
    sound_data = ListProperty(sound_names_list)

    def playMusic(self):

        #db.DatabaseInsertFile(str(mpb.soundFilePath), mpb.soundFile)
        mpb.soundFilePlay()
        print(self.soundName)
        self.soundNameChange()

        # Adding the song to the playlist

    def pauseMusic(self):

        # Pause the sound currently being played
        mpb.soundFilePause()

    def soundNameChange(self):

        # This function changes the label to the song
        # we are playing at that moment
        self.soundName = mpb.soundFile

    def insertToDatabase(self):

        if mpb.soundFilePath:
            # Arguments are taken from MusicPlayerBackend
            db.DatabaseInsertFile(str(mpb.soundFilePath), mpb.soundFile)
            self.sound_data.append(str(self.soundName))
        else:
            print("Can't insert an empty file")


class FileChooserScreen(Screen):


    # File we are going to play
    soundFile = ""

    def selectFile(self, *args):
        try:
            self.label.text = args[1][0]
            mpb.soundFileLoader(args[1][0])
        except:
            pass


sm = ScreenManager()
sm.add_widget(MainMenuScreen(name="main_menu"))
sm.add_widget(MusicScreen(name="music"))
sm.add_widget(FileChooserScreen(name="file_chooser"))


class MusicPlayerFrontendApp(App):
    def build(self):
        self.title = "Music Player"
        return sm


if __name__ == "__main__":
    MusicPlayerFrontendApp().run()