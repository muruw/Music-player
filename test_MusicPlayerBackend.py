import unittest
import MusicPlayerBackend

db = MusicPlayerBackend.Database()

class Testdb(unittest.TestCase):

    def test_ListViewObjects(self):
        result = db.ListViewObjects()
        self.assertEqual(result, {'<kivy.core.audio.audio_gstplayer.SoundGstplayer object at 0x000002E5796C7388>': 'titanium.ogg', '<kivy.core.audio.audio_gstplayer.SoundGstplayer object at 0x000002E579782E80>': 'ShortMusic.mp3', 'None': '', '<kivy.core.audio.audio_gstplayer.SoundGstplayer object at 0x0000019661300118>': '', '<kivy.core.audio.audio_gstplayer.SoundGstplayer object at 0x0000019660CD0E80>': 'ShortMusic.mp3', '<kivy.core.audio.audio_gstplayer.SoundGstplayer object at 0x10E9BF80>': ''})


if __name__ == "__main__":
    unittest.main()