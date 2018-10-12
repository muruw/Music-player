from kivy.core.audio import SoundLoader

class MusicPlayerBackend:

    def __init__(self):
        pass
    
    def writeHello(self, helloString):
        return helloString
    
    def soundFilePlay(self, soundFileNameString):
        soundFile = SoundLoader.load(soundFileNameString)
        if soundFile:
            print("Sound found at %s" % soundFile.source)
            print("Sound is %.3f seconds" % soundFile.length)
            return soundFile.play()
            
        