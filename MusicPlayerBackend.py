from kivy.core.audio import SoundLoader

from pathlib import Path

class MusicPlayerBackend:

    # The file we are currently playing
    soundFile = ""
    soundFilePath = ""

    def __init__(self):
        pass
    
    def soundFilePlay(self):
        soundName = self.soundFilePath
        try:
            print("Sound found at %s" % soundName.source)
            print("Sound is %.3f seconds" % soundName.length)
            self.soundFile = (Path(soundName.source).parts)[-1]
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
        self.soundFilePath = SoundLoader.load(soundName)
        
        return self.soundFile

    


        
    
        
        
            
            
        