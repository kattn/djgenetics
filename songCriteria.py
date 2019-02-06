import config as cf

def songLengthRule(song):
    if len(song) > cf.songLength:
        return -100
    else:
        return 0

# Illegal jumps in pitch
# Pattern maching
# Suspension
# First downbeat
# Thirds downbeat
# Long notes
# Pitch contour
# Speed
# Base drop