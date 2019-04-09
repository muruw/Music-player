import sqlite3
import vlc
# vlc requires import time
import time
from pathlib import Path


class MusicPlayerBackend:

    def __init__(self):

        self.trackName = ""
        self.trackPath = None
        self.sound_file = None

    def get_file_path(self, path):

        self.trackPath = path
        self.trackName = Path(self.trackPath).parts[-1]

    def get_sound_file(self, path):

        sound_file = vlc.MediaPlayer(path)
        self.sound_file = sound_file

    def track_play(self, sound_file):

        sound_file.stop()
        sound_file.play()

    def track_pause(self, sf):
        if sf == None:
            print("Nothing to stop")
        else:
            print(self.sound_file)
            sf.stop()


class Database:

    def __init__(self):

        self.databaseConnection = sqlite3.connect("MusicPlayerDatabase.db")
        self.cursor = self.databaseConnection.cursor()

    def DatabaseSetup(self):

        try:
            self.databaseConnection.execute(
                "CREATE TABLE IF NOT EXISTS MusicFiles (ID INTEGER PRIMARY KEY AUTOINCREMENT,"
                "fileLocation TEXT, fileName TEXT);")

            self.databaseConnection.commit()
            print("Database has been created INFO 01: DatabaseSetup()")

        except:
            print("Database was not found ERROR 01: DatabaseSetup()")

    def DatabaseInsertFile(self, fileLocation, fileName):

        self.databaseConnection.execute("INSERT INTO MusicFiles(fileLocation, fileName) VALUES ('" +
                                        fileLocation + "', '" +
                                        fileName + "')")
        print("Commit successful INFO 02: DatabaseInsertFile()")
        self.databaseConnection.commit()

    def ListViewObjects(self):

        data_items = {}
        try:
            result = self.cursor.execute("SELECT fileLocation, fileName FROM MusicFiles")

            for data in result:
                data_items[data[0]] = data[1]
        except:
            pass
        return data_items

    def getSoundLocation(self, sound_name):

        try:
            self.cursor.execute("SELECT fileLocation FROM MusicFiles WHERE filename = ?", (sound_name,))
            result = self.cursor.fetchone()

            track_path = result[0]
            return track_path
        except:
            pass

    def DatabaseCheckFile(self, file_name):

        self.cursor.execute("SELECT fileName FROM MusicFiles")
        result = self.cursor.fetchall()

        search_value = (file_name,)
        print(search_value)

        if search_value not in result:
            return True
        return False