from kivy.core.audio import SoundLoader

import sqlite3

from pathlib import Path


class MusicPlayerBackend:

    # The file we are currently playing
    soundFile = ""
    soundFilePath = None

    def soundFilePlay(self):
        soundName = self.soundFilePath
        try:
            #self.soundFile = Path(soundName.source).parts[-1]

            print("Sound found at %s" % soundName.source)
            print("Sound is %.3f seconds" % soundName.length)

            # The sound plays til it's stopped 
            soundName.loop = True
            soundName.play()
            print("Playfile: " + str(soundName.state))

        except:
            pass

    def soundFilePause(self):
        sound = self.soundFilePath

        # We must pass the error if sound == "", otherwise the application would crash
        try:
            if sound.state == "play":
                sound.stop()
                print("SoundFilePause() " + sound.state)
        except:
            pass

    def soundFileLoader(self, soundName):

        # This function will preload the given song

        # We will check whether the song is already playing to avoid music overlapping
        if not self.soundFilePath:
            self.soundFilePath = SoundLoader.load(soundName)
            # Path().parts creates a list from a file's path and we will get the
            # last element in that list, which equals to the file's name
            self.soundFile = Path(self.soundFilePath.source).parts[-1]
        else:
            self.soundFilePath.stop()
            self.soundFilePath = SoundLoader.load(soundName)
            self.soundFile = Path(self.soundFilePath.source).parts[-1]
            print("State = play")

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
        print(MusicPlayerBackend.soundFilePath)
        print("Commit successful INFO 02: DatabaseInsertFile()")
        self.databaseConnection.commit()

    def DatabaseCheckFile(self, file_name):

        self.cursor.execute("SELECT fileName FROM MusicFiles")
        result = self.cursor.fetchall()
        print(result)

        search_value = (file_name,)
        print(search_value)

        if search_value not in result:
            return True
        else:
            print("ERROR: DatabaseCheckFile() File already in playlist")
            return False

    def ListViewObjects(self):

        data_items = {}
        try:
            result = self.cursor.execute("SELECT fileLocation, fileName FROM MusicFiles")
            for data in result:
                data_items[data[0]] = data[1]
        except:
            pass

        print(data_items)
        return data_items

    def getSoundLocation(self, sound_name):

        try:
            result = self.cursor.execute("SELECT fileLocation FROM MusicFiles WHERE fileName = ?", sound_name)
            MusicPlayerBackend().soundFilePath = result
        except:
            pass
