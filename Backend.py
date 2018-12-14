from kivy.core.audio import SoundLoader

import sqlite3

from pathlib import Path


class MusicPlayerBackend:

    trackName = ""
    trackPath = None
    gst_object = None

    def return_variables(self):
        variables = (self.trackName, self.trackPath, self.gst_object)
        return variables

    def file_loader(self, file_path):

        """
        If gst_object isn't None, then we can use stop() to make sure
        the track isn't playing
        """

        if self.gst_object is not None:
            self.gst_object.stop()

        self.trackPath = file_path
        self.trackName = Path(file_path).parts[-1]
        print("file_loader() :", str(self.trackName))
        self.gst_object = SoundLoader.load(file_path)
        print("file_loader() : File location is " + str(file_path))
        print("file_loader() : gStreamer obj is now " + str(self.gst_object))

    def return_gst_obj(self):

        """
        The only reason we are creating this function is to get the same
        id of the gst_obj for track_play() and track_pause()
        """
        gst_obj = self.gst_object
        print(id(gst_obj))
        return gst_obj

    def track_play(self, gst_obj):
        try:
            print("Sound found at %s" % gst_obj.source)
            print("Sound is %.3f seconds" % gst_obj.length)
            """
            We will change the trackName variable to the current track's name
            Additionally, we are using the self.gst_object to play music.
            """
            self.trackName = Path(gst_obj.source).parts[-1]
            print("track_play() :", str(self.trackName))
            gst_obj.loop = True
            gst_obj.play()
            print(id(gst_obj))

        except:
            print("track_play() ERROR : gst_object wrong type")

    def track_pause(self, gst_obj):
        print("dir used:", str(dir()))
        print("globals used:", str(globals()))
        print("locals used:", str(locals()))
        try:

            gst_obj.stop()

        except:
            print("track_pause() ERROR : gst_object wrong type")


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
        print(sound_name)
        try:
            self.cursor.execute("SELECT fileLocation FROM MusicFiles WHERE filename = ?", (sound_name,))
            result = self.cursor.fetchone()
            print(result)
            print("get_sound_location() :", str(result))

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
