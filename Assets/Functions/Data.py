import win32clipboard
import random


def shorten_int(data, length, pd):
    if data > length:
        return str(pd)
    elif data < length:
        return str(length)


def shorten_string(data, length):
    if len(data) > length:
        return data[:length - 5] + "....."
    elif len(data) < length:
        return data



def get_standard_size(size, typ="short"):
    size = int(size)
    """Telly App internal functions
    this generates the appropriate standard size for the sizes """
    if typ == "short":
        holders = ['b', 'KB', 'MB', 'GB', 'TB']
        for x in holders:
            if size < 1024.0:
                return "%3.1f %s" % (size, x)
            size /= 1024.0
        return size
    elif typ == "long":
        holders = ['bytes', 'KB', 'MB', 'GB', 'TB']
        for x in holders:
            if size < 1024.0:
                return "%3.1f %s" % (size, x)
            size /= 1024.0
        return size


def paste_data():
    win32clipboard.OpenClipboard()
    try:
        data = win32clipboard.GetClipboardData()
    except Exception as s:
        str(s.args)
        data = ""
    win32clipboard.CloseClipboard()
    return data


def copy_data(data):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(data)
    win32clipboard.CloseClipboard()


def check_type(d_type, f_extension=None):
    d_type = d_type.lower()
    if "application" in d_type:
        if f_extension == "exe" or f_extension == "msi":
            img = "Assets/Media/app.png"
            return img
        else:
            img = "Assets/Media/app.png"
            return img
    elif "audio" in d_type:
        img = "Assets/Media/audio.png"
        return img
    elif "font" in d_type:
        img = "Assets/Media/font.png"
        return img
    elif "image" in d_type:
        img = "Assets/Media/picture.png"
        return img
    elif "video" in d_type:
        img = "Assets/Media/video.png"
        return img
    elif "text" in d_type:
        img = "Assets/Media/document.png"
        return img
    elif f_extension == "telly":
        img = "Assets/Media/unrecognized.png"
        return img
    else:
        img = "Assets/Media/unrecognized.png"
        return img


def create_random_characters():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z']
    numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', ]
    choice = random.choice([letters, numbers])
    a = random.choice(choice)
    choice = random.choice([letters, numbers])
    b = random.choice(choice)
    choice = random.choice([letters, numbers])
    c = random.choice(choice)
    choice = random.choice([letters, numbers])
    d = random.choice(choice)
    choice = random.choice([letters, numbers])
    e = random.choice(choice)
    ran_characters = a + b + c + d + e
    return ran_characters
