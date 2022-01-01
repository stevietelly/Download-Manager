import Assets.Functions.Parser as p
from Graphics.Popups import SnackBar
from Graphics.Colors import get_main_theme_color

from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.switch import Switch
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

import tkinter as tk
from tkinter import filedialog

all_settings_tab = []

""" the setting for checking internet connection"""

internet_tab = BoxLayout(size_hint=(1, None), height=dp(40), spacing=(5, 5))

int_box_a = BoxLayout(size_hint=(.4, 1))
int_box_a.add_widget(
    Label(text="Always check for internet connection", size_hint=(None, None), pos_hint={'x': 0, 'y': .15},
          color="04B5E6", halign="left", font_name="Assets/Fonts/DroidSans.ttf", width=dp(265), height=dp(25)))

""" Checking for internet Connection"""
int_box_b = BoxLayout(size_hint=(.6, 1))
int_switch = Switch(size_hint=(None, None), pos_hint={'x': 0, 'y': .15}, width=dp(80), height=dp(25),
                    active=p.KeyMatch().match("internet_validation"))
int_box_b.add_widget(int_switch)

internet_tab.add_widget(int_box_a)
internet_tab.add_widget(int_box_b)

all_settings_tab.append(internet_tab)

"""the setting for checking for the validity of the url"""

url_valid_tab = BoxLayout(size_hint=(1, None), height=dp(40))

url_box_a = BoxLayout(size_hint=(.4, 1))
url_box_a.add_widget(
    Label(text="Always Validate link", pos_hint={'x': 0, 'y': .15}, size_hint=(None, None), color="04B5E6",
          font_name="Assets/Fonts/DroidSans.ttf", halign="left", width=dp(150), height=dp(25)))

"""link_validation"""
url_box_b = BoxLayout(size_hint=(.6, 1))
valid_switch = Switch(pos_hint={'x': 0, 'y': .15}, size_hint=(None, None), active=p.KeyMatch().match("link_validation"),
                      width=dp(80), height=dp(25))
url_box_b.add_widget(valid_switch)
url_valid_tab.add_widget(url_box_a)
url_valid_tab.add_widget(url_box_b)

all_settings_tab.append(url_valid_tab)

""" the settings for the download directory """
directory_tab = BoxLayout(size_hint=(1, None), height=dp(40))

dir_tab_a = BoxLayout(size_hint=(.4, 1))
dir_tab_a.add_widget(Label(
    text="Download Directory", pos_hint={'x': 0, 'y': .15}, size_hint=(None, None), height=dp(25), width=dp(150),
    color="04B5E6", font_name="Assets/Fonts/DroidSans.ttf"))

"""directory"""
dir_tab_b = BoxLayout(size_hint=(.6, 1))
dir_input = TextInput(pos_hint={'x': 0, 'y': .05}, size_hint=(None, None), multiline=False, width=dp(400),
                      height=dp(30), text=p.KeyMatch().match("directory"))

choose = Button(text="Change", size_hint=(None, None), pos_hint={'x': 0, 'y': .05}, height=dp(30), width=dp(70),
                on_press=lambda obj: change_directory())

dir_tab_b.add_widget(dir_input)
dir_tab_b.add_widget(Widget())
dir_tab_b.add_widget(choose)
dir_tab_b.add_widget(Widget())

directory_tab.add_widget(dir_tab_a)
directory_tab.add_widget(dir_tab_b)

all_settings_tab.append(directory_tab)

"""the setting for approval before downloading """

down_approve_tab = BoxLayout(size_hint=(1, None), height=dp(40))

approve_tab_a = BoxLayout(size_hint=(.4, 1))
approve_tab_a.add_widget(
    Label(text="Ask before downloading", pos_hint={'x': 0, 'y': .15}, size_hint=(None, None), height=dp(25),
          width=dp(180), font_name="Assets/Fonts/DroidSans.ttf", halign="left", color="04B5E6"))

"""approval"""
approve_tab_b = BoxLayout(size_hint=(.6, 1))
approve_switch = Switch(pos_hint={'x': 0, 'y': .15}, size_hint=(None, None), active=p.KeyMatch().match("approval"),
                        width=dp(80), height=dp(25))

approve_tab_b.add_widget(approve_switch)

down_approve_tab.add_widget(approve_tab_a)
down_approve_tab.add_widget(approve_tab_b)

all_settings_tab.append(down_approve_tab)

"""the setting for warning before cancelling download"""

warn_tab = BoxLayout(size_hint=(1, None), height=dp(40))

warn_box_a = BoxLayout(size_hint=(.4, 1))
warn_box_a.add_widget(
    Label(text="Warn before terminating download", pos_hint={'x': 0, 'y': .15}, height=dp(25), width=dp(250),
          color="04B5E6", halign="left", size_hint=(None, None), font_name="Assets/Fonts/DroidSans.ttf"))

"""warning"""
warn_box_b = BoxLayout(size_hint=(.6, 1))
warn_switch = Switch(pos_hint={'x': 0, 'y': .15}, height=dp(25), width=dp(80), size_hint=(None, None),
                     active=p.KeyMatch().match("warning"))

warn_box_b.add_widget(warn_switch)
warn_tab.add_widget(warn_box_a)
warn_tab.add_widget(warn_box_b)

all_settings_tab.append(warn_tab)

"""the setting for the app theme"""

theme_tab = BoxLayout(size_hint=(1, None), height=dp(40))

theme_box_a = BoxLayout(size_hint=(.4, 1))
theme_box_a.add_widget(
    Label(text="App theme", pos_hint={'x': 0, 'y': .15}, height=dp(25), width=dp(90), color="04B5E6", halign="left",
          size_hint=(None, None), font_name="Assets/Fonts/DroidSans.ttf"))

"""theme"""
theme_box_b = BoxLayout(size_hint=(.6, 1))
theme_input = TextInput(pos_hint={'x': 0, 'y': .05}, size_hint=(None, None), multiline=False, width=dp(400),
                        height=dp(30), text=p.KeyMatch().match("theme"))

theme_box_b.add_widget(theme_input)
theme_box_b.add_widget(Widget())

theme_box_b.add_widget(
    Button(text="Change", size_hint=(None, None), pos_hint={'x': 0, 'y': .05}, height=dp(30), width=dp(70)))
theme_box_b.add_widget(Widget())

theme_tab.add_widget(theme_box_a)
theme_tab.add_widget(theme_box_b)

all_settings_tab.append(theme_tab)

"""the setting for notifications"""

notifications_tab = BoxLayout(size_hint=(1, None), height=dp(40))

notifications_box_a = BoxLayout(size_hint=(.4, 1))
notifications_box_a.add_widget(
    Label(text="Always show notifications", pos_hint={'x': 0, 'y': .15}, height=dp(25), width=dp(190), color="04B5E6",
          halign="left", size_hint=(None, None), font_name="Assets/Fonts/DroidSans.ttf"))

"""notifications"""
notifications_box_b = BoxLayout(size_hint=(.6, 1))
notifications_switch = Switch(pos_hint={'x': 0, 'y': .15}, size_hint=(None, None), height=dp(25), width=dp(80),
                              active=p.KeyMatch().match("notifications"))

notifications_box_b.add_widget(notifications_switch)
notifications_tab.add_widget(notifications_box_a)
notifications_tab.add_widget(notifications_box_b)

all_settings_tab.append(notifications_tab)

"""the setting for notifying before saving settings"""

ask_tab = BoxLayout(size_hint=(1, None), height=dp(40))

ask_box_a = BoxLayout(size_hint=(.4, 1))
ask_box_a.add_widget(
    Label(text="Always ask before saving settings", pos_hint={'x': 0, 'y': .15}, height=dp(25), width=dp(234),
          color="04B5E6", halign="left", size_hint=(None, None), font_name="Assets/fonts/DroidSans.ttf"))

"""warn_settings"""
ask_box_b = BoxLayout(size_hint=(.6, 1))
ask_switch = Switch(pos_hint={'x': 0, 'y': .15}, size_hint=(None, None), active=p.KeyMatch().match("warn_settings"),
                    width=dp(80), height=dp(25))

ask_box_b.add_widget(ask_switch)

ask_tab.add_widget(ask_box_a)
ask_tab.add_widget(ask_box_b)

all_settings_tab.append(ask_tab)

"""the setting for beeping after download finish"""

beep_finish_tab = BoxLayout(size_hint=(1, None), height=dp(40))

beep_finish_box_a = BoxLayout(size_hint=(.4, 1))
beep_finish_box_a.add_widget(
    Label(text="Beep after download has finished", pos_hint={'x': 0, 'y': .15}, height=dp(25), width=dp(250),
          color="04B5E6", halign="left", size_hint=(None, None), font_name="Assets/Fonts/DroidSans.ttf"))

"""beep_finish"""
beep_finish_box_b = BoxLayout(size_hint=(.6, 1))
beep_finish_switch = Switch(pos_hint={'x': 0, 'y': .15}, height=dp(25), width=dp(80), size_hint=(None, None),
                            active=p.KeyMatch().match("beep_finish"))

beep_finish_box_b.add_widget(beep_finish_switch)

beep_finish_tab.add_widget(beep_finish_box_a)
beep_finish_tab.add_widget(beep_finish_box_b)

all_settings_tab.append(beep_finish_tab)

"""the setting for beep when error occurs"""

beep_error_tab = BoxLayout(size_hint=(1, None), height=dp(40))

beep_error_box_a = BoxLayout(size_hint=(.4, 1))
beep_error_box_a.add_widget(
    Label(text="Beep when an error occurs", height=dp(25), width=dp(200), color="04B5E6", halign="left",
          pos_hint={'x': 0, 'y': .15}, size_hint=(None, None), font_name="Assets/Fonts/DroidSans.ttf"))

"""beep_error"""
beep_error_box_b = BoxLayout(size_hint=(.6, 1))
beep_error_switch = Switch(pos_hint={'x': 0, 'y': .15}, size_hint=(None, None), height=dp(25), width=dp(80),
                           active=p.KeyMatch().match("beep_error"))

beep_error_box_b.add_widget(beep_error_switch)

beep_error_tab.add_widget(beep_error_box_a)
beep_error_tab.add_widget(beep_error_box_b)

all_settings_tab.append(beep_error_tab)

"""the setting for saving all download procedures"""

download_save_tab = BoxLayout(size_hint=(1, None), height=dp(40))

download_save_box_a = BoxLayout(size_hint=(.4, 1))
download_save_box_a.add_widget(
    Label(text="Confirm before delete", pos_hint={'x': 0, 'y': .15}, height=dp(25), width=dp(240), color="04B5E6",
          halign="left", size_hint=(None, None), font_name="Assets/Fonts/DroidSans.ttf"))

"""save_down_proc"""
download_save_box_b = BoxLayout(size_hint=(.6, 1))
download_save_switch = Switch(pos_hint={'x': 0, 'y': .15}, height=dp(25), width=dp(80), size_hint=(None, None),
                              active=p.KeyMatch().match("save_down_proc"))

download_save_box_b.add_widget(download_save_switch)

download_save_tab.add_widget(download_save_box_a)
download_save_tab.add_widget(download_save_box_b)

all_settings_tab.append(download_save_tab)

""" Concurrent Downloads"""
con_down_tab = BoxLayout(size_hint=(1, .4), height=dp(40))

conc_tab_a = BoxLayout(size_hint=(.4, 1))
conc_tab_a.add_widget(
    Label(text="Concurrent Downloads", pos_hint={'x': 0, 'y': .15}, color="04B5E6", width=dp(170), height=dp(25),
          size_hint=(None, None), font_name="Assets/Fonts/DroidSans.ttf"))

""" concurrency_limit """
conc_tab_b = BoxLayout(size_hint=(.6, 1))

conc_input = TextInput(pos_hint={'x': 0, 'y': .05}, size_hint=(None, None), multiline=False, height=dp(30),
                       width=dp(100), text=str(p.KeyMatch().match("concurrency_limit")))

change = Button(text="Change", size_hint=(None, None), pos_hint={'x': 0, 'y': .05}, width=dp(70), height=dp(30))

conc_tab_b.add_widget(conc_input)
conc_tab_b.add_widget(Widget())
conc_tab_b.add_widget(change)
conc_tab_b.add_widget(Widget())

con_down_tab.add_widget(conc_tab_a)
con_down_tab.add_widget(conc_tab_b)

all_settings_tab.append(con_down_tab)


def change_directory():
    root = tk.Tk()
    root.iconbitmap("Assets/Media/downloader.ico")
    root.withdraw()
    folder = filedialog.askdirectory()
    if folder == "" or folder is None:
        dir_input.text = p.KeyMatch().match("directory")
        SnackBar(essence="info", message="Directory reverted to original", bg_color=get_main_theme_color("tuple"))

    else:
        dir_input.text = folder
        SnackBar(essence="info", message="Directory changed", bg_color=get_main_theme_color("tuple"))
