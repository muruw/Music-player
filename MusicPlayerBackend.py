from kivy.core.audio import SoundLoader



class MusicPlayerBackend:

    def __init__(self):
        pass
    
    def writeHello(self, helloString):
        return helloString
    
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
        print(sound.state)
        
        if sound.state == "play":
            sound.stop()
    
    def soundFileLoader(self):
        # Let's put all the songs into a dictionary,
        # later we will use filechooser to access this function
        soundFilesDict = {}
        soundFilesDict[0] = SoundLoader.load("titanium.ogg")
        print(soundFilesDict)
        return soundFilesDict
    
    def soundFileNameLoader(self):
        soundFileNameDict = {}
        soundFileNameDict[0] = "titanium.ogg"
        
        return soundFileNameDict
    


        
    
        
        
            
            
        