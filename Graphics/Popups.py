from kivy.metrics import dp
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivymd.uix.snackbar import Snackbar
import Assets.Functions.Parser as p
import Assets.Sound.Sound as s
import importlib
import threading


class PopupBox:
    def __init__(self, essence="warn", title="", error_code="", size=None, size_hint=None,
                 message="", icon="", escape=True, bg_color="#FFFFF", beep=False):
        """For the internal working of the app, this class is used to generate customized popups for
        the Telly app, the essence is to gve an overview of the type of popup required divided into
        three categories, the warn popup, the info popup and the central popup"""
        self.essence = essence
        self.title = title
        self.error = error_code
        self.icon = icon
        self.message = message
        self.count = 0
        self.bg_color = bg_color
        self.box = Popup()
        importlib.reload(p)

        # sizing the popup
        if size:
            self.box.size_hint = (None, None)
            self.box.size = size
        elif not size and size_hint:
            self.box.size_hint = size_hint

        else:
            self.box.size_hint = (.6, .4)

        # auto dismissing capabilities

        if escape:
            self.box.auto_dismiss = True
        elif not escape:
            self.box.auto_dismiss = False

        if beep:
            if p.KeyMatch().match("beep_error"):
                threading.Thread(target=lambda: s.beep()).start()

        self.box.background = ""
        self.box.title = title
        self.box.title_color = "D3D1FF"
        

    def warning_popup(self):
        self.box.title_color = "FF0114"
        self.box.separator_color = "FF0114"
        if self.error:
            self.box.title = "Warning: " + str(self.error)
        elif not self.error:
            self.box.title = "Warning: Error"
        self.box.background_color = "#FBFFF8"

        warner_cont = FloatLayout()
        img = Image()

        if self.icon:
            img.source = self.icon
        elif not self.icon:
            img.source = "Assets/Media/attention.png"

        img.size_hint = (None, None)
        img.size = (60, 60)
        img.pos_hint = {'x': 0, 'y': .4}
        warner_label = Label(halign="center")

        if self.message:
            warner_label.text = str(self.message) + ": " + str(self.error)
        elif not self.message:
            warner_label.text = "An issue was encountered: " + str(self.error)

        warner_label.size_hint = (None, None)
        warner_label.width = dp(100)
        warner_label.height = dp(40)
        warner_label.color = "FF0114"
        warner_label.font_size = 20
        warner_label.pos_hint = {'x': .45, 'y': .5}

        warner_cont.add_widget(img)
        warner_cont.add_widget(warner_label)
        self.box.content = warner_cont

    def info_popup(self):
        self.box.title_font = "Assets/fonts/inconsolata.ttf"
        self.box.background_color = "#FF667F"
        self.box.title = self.title
        cont = FloatLayout()
        icon = Image()
        if self.icon:
            icon.source = self.icon
        elif not self.icon:
            icon.source = "Assets/icons/check.png"
        icon.size_hint = (None, None)
        icon.size = (50, 50)
        icon.pos_hint = {'x': 0, 'y': .4}
        infolabel = Label(halign="center")

        if self.message:
            infolabel.text = str(self.message)
        elif not self.message:
            infolabel.text = "Success"

        infolabel.size_hint = (None, None)
        infolabel.width = dp(100)
        infolabel.height = dp(40)
        infolabel.font_size = 22
        infolabel.pos_hint = {'x': .45, 'y': .5}

        cont.add_widget(infolabel)
        cont.add_widget(icon)
        self.box.content = cont

    def central_popup(self):
        self.box.title = self.title
        self.box.background_color = self.bg_color
        self.box.separator_color = "#FFFFFF"

    def pop(self):
        if self.essence == "warn":
            """with this type of essence the title is generally limited"""
            self.warning_popup()

        if self.essence == "info":
            self.info_popup()

        if self.essence == "central":
            self.central_popup()

        threading.Thread(self.box.open()).start()

    def content(self, content=None):

        if self.essence == "central":
            "only the central essence is allowed to have its own content"
            if content:
                self.box.content = content
            elif not content:
                pass
        else:
            pass

    def color(self, color, dt=None):
        self.box.background_color = color

    def exit(self):
        self.box.dismiss()


class SnackBar:
    def __init__(self, essence="info", message=str, bg_color=(.16, .55, 1, .2)):
        """ snackbars are important for conveying information """
        importlib.reload(p)
        self.box = Snackbar()
        self.box.duration = 1
        self.box.auto_dismiss = True
        self.box.min_state_time = 1
        bg_color = list(bg_color)
        bg_color[3] = .2
        if essence == "info":
            self.box.text = message
            self.box.md_bg_color = bg_color
            self.box.snackbar_x = dp(10)
            self.box.snackbar_y = dp(10)
            self.box.size_hint = (None, None)
            self.box.height = dp(70)
            self.box.width = dp(250)
            self.box.pos_hint = {'x': .7}
            threading.Thread(self.box.open()).start()

        elif essence == "extra":
            if p.KeyMatch().match("notifications"):
                self.box.text = message
                self.box.md_bg_color = bg_color
                self.box.snackbar_x = dp(10)
                self.box.snackbar_y = dp(10)
                self.box.size_hint = (.5, .1)
                self.box.pos_hint = {'x': .7}
                threading.Thread(self.box.open()).start()
            elif not p.KeyMatch().match("notifications"):
                pass
