import winsound


def beep():
    """ Telly App internal functions
     this works for windows os  only it is a small beep announcing a new occurrence"""
    winsound.PlaySound("SystemQuestion", winsound.SND_ALIAS)
