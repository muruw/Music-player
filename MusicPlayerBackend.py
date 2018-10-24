from kivy.core.audio import SoundLoader

from pathlib import Path

class MusicPlayerBackend:

    soundFile = ""

    def __init__(self):
        pass
    
    def soundFilePlay(self, soundFileNameString):
        soundFile = soundFileNameString
        if soundFile is not None:
            print("Sound found at %s" % soundFile.source)
            print("Sound is %.3f seconds" % soundFile.length)
            # The sound plays til it's stopped 
            soundFile.loop = True
            soundFile.play()
            print(soundFile.state)
        
    
    def soundFilePause(self, soundFileStr):
        sound = soundFileStr
        
        if sound.state == "play":
            sound.stop()
            print(sound.state)
            
    def soundFileLoader(self, soundName):
        
        # This function will preload the given song
        self.soundFile = SoundLoader.load(soundName)
        
        return self.soundFile
    
    def soundFileNameLoader(self, soundName):
        correctedFileName = Path(soundName.source).parts
        
        return correctedFileName[-1]
    


        
    
        
        
            
            
        