import kivy
import Backend
import time
import vlc
import threading

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

    selected_value = StringProperty("Select a song")

    sound_data = ListProperty(sound_names_list)
    soundName = StringProperty("Select a song")
    # A reference to the trackName

    def play_from_playlist(self, track_name):

        self.selected_value = "Selected: {}".format(track_name)
        print(self.selected_value)
        track_path = db.getSoundLocation(track_name)
        mpb.file_loader(track_path)
        mpb.track_play(mpb.gst_object)

    def playMusic(self):
        print("gst_obj: " + str(mpb.gst_object))
        mpb.track_play(mpb.return_gst_obj())
        print("playMusic(): ", str(mpb.trackName))

    def play_button_pressed(self):
        self.selected_value = mpb.trackName

    def pauseMusic(self):

        mpb.track_pause(mpb.gst_object)

    def insertToDatabase(self):

        if mpb.trackName != "":
            if db.DatabaseCheckFile(str(mpb.trackName)):
                db.DatabaseInsertFile((str(mpb.trackPath)), str(mpb.trackName))
                #self.sound_data.append(str(mpb.trackName))
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

    def app_play_radio(self):
        self.radio = RadioThread(self.play_radio)
        self.radio.start()

    def app_stop_radio(self):
        self.radio.stop()
        self.sound_file.stop()

    def play_radio(self):
        self.sound_file = vlc.MediaPlayer(self.raadiod[0])
        self.sound_file.play()
        while True:
            time.sleep(0.5)



"""
class RadioScreen(Screen):

    raadiod = [
    "http://skyplus.babahhcdn.com/SKYPLUS",
    "http://striiming.trio.ee/elmar.mp3",
    "http://striiming.trio.ee/myhits.mp3",
    "http://icecast.err.ee/raadio2.mp3",
    "http://skyplus.babahhcdn.com:7004/NRJ",
    ]
    index = 0
    sound_file = vlc.MediaPlayer(raadiod[index])
    radio_status = False

    def play_radio(self):
        while self.radio_status == True:
            self.sound_file.play()
        time.sleep(0.05)
    def stop_radio(self):

        self.radio_status = False

    def start_thread(self, index):

        self.sound_file = vlc.MediaPlayer(self.raadiod[index])
        self.radio_status = True
        self.t1 = threading.Thread(target=self.play_radio)
        self.t1.start()


class Radio(threading.Thread):

    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        time.sleep(5)
        self.queue.put("Task finished")
"""
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
