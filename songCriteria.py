import config as cf

def songLengthRule(song):
    if len(song) > cf.songLength:
        return -100
    else:
        return 0