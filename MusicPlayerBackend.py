from kivy.core.audio import SoundLoader

import sqlite3

from pathlib import Path


class MusicPlayerBackend:

    # The file we are currently playing
    soundFile = ""
    soundFilePath = ""

    def soundFilePlay(self):
        soundName = self.soundFilePath
        try:
            self.soundFile = Path(soundName.source).parts[-1]

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
        if self.soundFilePath == "":
            self.soundFilePath = SoundLoader.load(soundName)
        else:
            self.soundFilePath.state = "stop"
            self.soundFilePath = SoundLoader.load(soundName)
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
