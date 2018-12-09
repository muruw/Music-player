from random import randint

from kivy.core.audio import SoundLoader

heli = SoundLoader.load("C:\Users\Marcus\Desktop\titanium.ogg")

while True:
    userInput = input("Vajuta enter: ")
    if userInput == "":
        heli.play()
