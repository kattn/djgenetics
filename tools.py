import pygame

''' pygame.mixer doesn't work with arch atm, play midis through timidity

freq = 44100
bitsize = -16
channels = 2
buffer = 1024
pygame.mixer.init(freq, bitsize, channels, buffer)
    
def playMidiFile(pathToMidiFile):
    pygame.mixer.music.load(pathToMidiFile)
    print("Loaded", pathToMidiFile)
    pygame.mixer.music.play()

def playImportedMidi(importedMidi):
    pass

def playRoll(roll):
    pass
'''

