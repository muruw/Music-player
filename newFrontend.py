import kivy
import NewBackend

# Use mpb to access backend methods
mpb = NewBackend.NewBackend()
db = NewBackend.Database()

kivy.require("1.10.0")

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
print("LVO: " + str(db.ListViewObjects()))


class MainMenuScreen(Screen):
    pass


class MusicScreen(Screen):

    sound_names_list = []
    soundDirectory = db.ListViewObjects()

    for sound_name in soundDirectory.items():
        sound_names_list.append(sound_name[1])

    sound_data = ListProperty(sound_names_list)

    soundName = StringProperty()

    def playMusic(self):

        mpb.track_play(mpb.gst_object)
        self.soundName = mpb.trackName

    def pauseMusic(self):

        mpb.track_pause(mpb.gst_object)

    def insertToDatabase(self):

        if db.DatabaseCheckFile(str(mpb.trackName)):
            db.DatabaseInsertFile(str(db.getSoundLocation(mpb.trackName)), str(mpb.trackName))
            self.sound_data.append(str(mpb.trackName))
            print("The track has been added to the playlist!")
        else:
            print("InsertToDatabase() : Couldn't add the track to the playlist :(")


class FileChooserScreen(Screen):

    def selectFile(self, *args):

        try:
            print(args[1][0])
            self.label.text = args[1][0]
            mpb.file_loader(args[1][0])
        except:
            pass


class PlaylistButton(ListItemButton):

    @staticmethod
    def get_button_index(index):

        db.getSoundLocation(MusicScreen().sound_data[index])
        file_path = str(mpb.trackPath)
        print("get_button_index() :", str(file_path))

        mpb.file_loader(file_path)
        MusicScreen().playMusic()


sm = ScreenManager()
sm.add_widget(MainMenuScreen(name = "main_menu"))
sm.add_widget(MusicScreen(name = "music"))
sm.add_widget(FileChooserScreen(name = "file_chooser"))

class NewFrontendApp(App):
    def build(self):
        self.title = "MuBin"
        return sm

if __name__ == "__main__":
    NewFrontendApp().run()