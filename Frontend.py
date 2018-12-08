import kivy
import Backend

# Use mpb to access backend methods
mpb = Backend.MusicPlayerBackend()
db = Backend.Database()

kivy.require("1.10.0")
from random import randint
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.listview import ListItemButton

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


class MainMenuScreen(Screen):
    pass


class MusicScreen(Screen):

    sound_names_list = []
    soundDirectory = db.ListViewObjects()

    for sound_name in soundDirectory.items():
        sound_names_list.append(sound_name[1])

    sound_data = ListProperty(sound_names_list)
    soundName = StringProperty("")
    # A reference to the trackName
    track_name = mpb.trackName

    def playMusic(self):
        print("gst_obj: " + str(mpb.gst_object))
        mpb.track_play(mpb.return_gst_obj())
        print("playMusic(): ", str(mpb.trackName))
        self.soundName = mpb.trackName

    def pauseMusic(self):

        gst_obj_copy = mpb.return_gst_obj()
        mpb.track_pause(gst_obj_copy)

    def insertToDatabase(self):

        if mpb.trackName != "":
            if db.DatabaseCheckFile(str(mpb.trackName)):
                db.DatabaseInsertFile((str(mpb.trackPath)), str(mpb.trackName))
                self.sound_data.append(str(mpb.trackName))
                print("The track has been added to the playlist!")
            else:
                print("InsertToDatabase() : Couldn't add the track to the playlist :(")
        else:
            print("InsertToDatabase() : mpb.trackName is None")


class FileChooserScreen(Screen):

    def selectFile(self, *args):

        try:
            print(args[1][0])
            self.label.text = args[1][0]
            mpb.file_loader(args[1][0])
        except:
            pass


class PlaylistButton(ListItemButton):

    def get_button_index(self, index):

        db.getSoundLocation(MusicScreen().sound_data[index])
        file_path = str(mpb.trackPath)
        print("get_button_index() :", str(file_path))

        mpb.file_loader(file_path)
        #MusicScreen.soundName = mpb.trackName
        print("mpb.trackName = " + str(mpb.trackName))
        print("Name of the track" + str(MusicScreen.soundName))
        MusicScreen.playMusic(MusicScreen)


sm = ScreenManager()
sm.add_widget(MainMenuScreen(name = "main_menu"))
sm.add_widget(MusicScreen(name = "music"))
sm.add_widget(FileChooserScreen(name = "file_chooser"))


class FrontendApp(App):
    def build(self):
        self.title = "MuBin"
        return sm


if __name__ == "__main__":
    FrontendApp().run()
