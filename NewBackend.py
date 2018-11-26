from kivy.core.audio import SoundLoader

import sqlite3

from pathlib import Path


class NewBackend:

    trackName = ""
    trackPath = None
    gst_object = None

    def file_loader(self, file_path):
        if not self.gst_object:

            self.gst_object = SoundLoader.load(file_path)
            print("file_loader() : File location is " + str(file_path))

            #return self.gst_object
        else:
            self.gst_object.stop()
            self.gst_object = SoundLoader.load(file_path)
            print("file_loader() : File location is " + str(file_path))


    def track_play(self, gst_object):

        try:
            print("Sound found at %s" % gst_object.source)
            print("Sound is %.3f seconds" % gst_object.length)

            gst_object.loop = True
            gst_object.play()
            self.trackName = Path(gst_object.source).parts[-1]

        except:
            pass

    def track_pause(self, gst_object):

        if gst_object.state == "play":
            gst_object.stop()
        else:
            print(" track_pause : File is already paused.")


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
        print(data_items)
        return data_items

    def getSoundLocation(self, sound_name):
        print(sound_name)
        try:

            self.cursor.execute("SELECT fileLocation FROM MusicFiles WHERE filename = ?", (sound_name,))
            result = self.cursor.fetchone()
            print(result)
            print("get_sound_location() :", str(result) )
            NewBackend.trackPath = result[0]
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
