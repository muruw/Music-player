import kivy
import Backend
import time
import vlc
import threading
import copy

# Use mpb to access backend methods
mpb = Backend.MusicPlayerBackend()
db = Backend.Database()

kivy.require("1.10.0")

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty
from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.core.window import Window

Window.clearcolor = (1, 1, 1, 1)

# Locating all the .kv files
from os import listdir
"""
kv_path = "./kivyFiles/"
for kv in listdir(kv_path):
    print(kv)
    Builder.load_file(kv_path + kv)
"""
Builder.load_file("Screens.kv")

# We will initialize the database
db.DatabaseSetup()


class MainMenuScreen(Screen):
    pass


class MusicScreen(Screen):

    sound_names_list = []
    soundDirectory = db.ListViewObjects()

    for sound_name in soundDirectory.items():
        sound_names_list.append(sound_name[1])

    selected_value = StringProperty("Select a song")
    current_track_name = ""
    sound_data = ListProperty(sound_names_list)
    soundName = StringProperty("Select a song")
    # A reference to the trackName

    sound_file = None

    def play_from_playlist(self, track_name):
        """
        Please refer to MusicScreen().playMusic() as the functionality is the same.
        The only difference is on the first line where we declare track_path
        """
        track_path = db.getSoundLocation(track_name)
        mpb.get_sound_file(track_path)
        mpb.track_play(mpb.sound_file)
        print("Song played")

    def playMusic(self):
        """
        we are going to initialize VLC sound file with get_sound_file()
        and it changes the mpb.sound_file to the corresponding file, which
        we can later on use to play/stop music
        """
        mpb.get_sound_file(mpb.trackPath)

        mpb.track_play(mpb.sound_file)
        print("playMusic(): ", str(mpb.trackName))

    def pauseMusic(self):

        mpb.track_pause(mpb.sound_file)

    def sound_data_append(self):
        if mpb.trackName != "":
            self.sound_data.append(mpb.trackName)
        else:
            print("Nothing to insert to the database")

    def insertToDatabase(self):
        self.current_track_name = mpb.trackName
        if mpb.trackName != "":
            if db.DatabaseCheckFile(str(mpb.trackName)):
                db.DatabaseInsertFile((str(mpb.trackPath)), str(mpb.trackName))
                print("The track has been added to the playlist!")
            else:
                print("InsertToDatabase() : Couldn't add the track to the playlist :(")
        else:
            print("InsertToDatabase() : mpb.trackName is None")


class FileChooserScreen(Screen):

    def selectFile(self, *args):

        self.label.text = args[1][0]
        mpb.get_file_path(args[1][0])


class RadioThread(threading.Thread):
    def __init__(self, func):
        self.running = False
        self.func = func
        super(RadioThread, self).__init__()

    def start(self):
        self.running = True
        super(RadioThread, self).start()

    def run(self):
        while self.running:
            self.func()

    def stop(self):
        self.running = False


class RadioScreen(Screen):

    # An instance of this screen's thread
    raadiod = [
    "http://skyplus.babahhcdn.com/SKYPLUS",
    "http://striiming.trio.ee/elmar.mp3",
    "http://striiming.trio.ee/myhits.mp3",
    "http://icecast.err.ee/raadio2.mp3",
    "http://skyplus.babahhcdn.com:7004/NRJ",
    ]
    index = 0
    sound_file = vlc.MediaPlayer(raadiod[0])
    radio_status = False

    def app_play_radio(self, radio_index):
        self.index = radio_index

        self.radio = RadioThread(self.play_radio)
        self.radio.start()

    def app_stop_radio(self):
        self.radio.stop()
        self.sound_file.stop()

    def play_radio(self):
        self.sound_file = vlc.MediaPlayer(self.raadiod[self.index])
        self.sound_file.play()
        while True:
            time.sleep(0.5)


sm = ScreenManager()
sm.add_widget(MainMenuScreen(name = "main_menu"))
sm.add_widget(MusicScreen(name = "music"))
sm.add_widget(FileChooserScreen(name = "file_chooser"))
sm.add_widget(RadioScreen(name = "radio"))


class mainApp(App):
    def build(self):
        self.title = "MuBin"
        return sm


if __name__ == "__main__":
    mainApp().run()
