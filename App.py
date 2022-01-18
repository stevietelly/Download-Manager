from Graphics import Config
import datetime as dt
import importlib
import multiprocessing
import os
import platform
import threading
import tkinter as tk
from tkinter import filedialog

from kivy.clock import Clock
from kivy.lang.builder import Builder
from kivy.metrics import dp
from kivy.properties import ColorProperty, ObjectProperty
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.textfield import MDTextField
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.button import MDIconButton

import Assets.Functions.Parser as p
from Assets.Engine.Engine import TellyEngine
from Assets.Functions.Data import (check_type, copy_data,
                                   create_random_characters, get_standard_size,
                                   paste_data, shorten_int, shorten_string)
from Assets.Functions.Methods import do_nothing
from Assets.Functions.Networks import (check_link_validity,
                                       check_network_connection)
from Assets.Sound.Sound import beep

from Graphics.Buttons import FlatButton
from Graphics.Colors import (get_main_theme_color, get_sub_theme_color,
                             get_transparent_sub_theme_color)
from Graphics.Intuix.all_downloads_tab import (all_downloading,
                                               all_downloads_bg,
                                               all_downloads_box, all_error,
                                               all_finished, all_label,
                                               all_paused)
from Graphics.Intuix.downloading_tab import (downloading_all, downloading_bg,
                                             downloading_error,
                                             downloading_finished,
                                             downloading_label,
                                             downloading_paused)
from Graphics.Intuix.error_downloads import (error_all, error_bg,
                                             error_downloading, error_finished,
                                             error_label, error_paused)
from Graphics.Intuix.finished_downloads import (finished_all, finished_bg,
                                                finished_downloading,
                                                finished_error, finished_label,
                                                finished_paused)
from Graphics.Intuix.paused_downloads import (paused_all, paused_bg,
                                              paused_downloading, paused_error,
                                              paused_finished, paused_label)
from Graphics.Intuix.Settings import (affirm_settings, cancel_new_settings,
                                      restore_default_settings_query,
                                      save_new_settings_query,
                                      settings_bg_scroll)
from Graphics.Popups import PopupBox, SnackBar

Builder.load_string(
    """
<MainLayout>:
    canvas.before:
        Color:
            rgb: root.theme
        Rectangle:
            size: self.size"""
)


class MainLayout(BoxLayout):
    # important methods are defined for later use throughout the class

    # variables
    errors = 0
    finished = 0
    downloads = 0
    paused = 0
    app_version = Config.app_version
    in_service_pids = []

    # widgets
    manager = ScreenManager()
    con_label = Label()
    down_label = Label()
    download_frame = BoxLayout()
    finished_label = Label()
    error_label = Label()
    paused_label = Label()
    settings_holder = BoxLayout()
    download_frame_manager = ScreenManager()
    all_downloads_tab = Screen()
    downloading_tab = Screen()
    paused_download_tab = Screen()
    error_downloads_tab = Screen()
    finished_downloads_tab = Screen()
    history_holder = BoxLayout()

    # kivy based widgets
    drawer = ObjectProperty()
    theme = ColorProperty()
    navbar = ObjectProperty()
    nav_link = ObjectProperty()
    home = ObjectProperty()
    enter_bt = ObjectProperty()
    back_st = ObjectProperty()
    back_hst = ObjectProperty()
    back_hp = ObjectProperty()
    download_pop = ObjectProperty()
    url_box = ObjectProperty()
    dir_input = ObjectProperty()

    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)
        # the screen manager is added before hand
        self.add_widget(self.manager)

        # the individual screens are broken down to be added
        threading.Thread(self.home_tab_init()).start()
        threading.Thread(self.settings_tab_init()).start()
        threading.Thread(self.history_tab_init()).start()
        threading.Thread(self.help_tab_init()).start()
      

        # a timer is added to update the whole program in intervals of 1/99 seconds
        Clock.schedule_interval(self.app_essentials_update, 1 / 99)

    def home_tab_init(self):
        # home tab
        home_tab = Screen(name="home")
        self.manager.add_widget(home_tab)

        self.home = BoxLayout(orientation="vertical")

        self.navbar = MDCard()
        self.navbar.size_hint = (1, None)
        self.navbar.height = dp(40)
        self.home.add_widget(self.navbar)

        threading.Thread(self.navbar_init()).start()
        threading.Thread(self.top_bar_init()).start()
        threading.Thread(self.info_bar_init()).start()
        threading.Thread(self.download_frame_init()).start()

        home_tab.add_widget(self.home)

        # drawer
        self.drawer = MDNavigationDrawer()
        self.drawer.md_bg_color = (.16, .55, 1, .3)
        threading.Thread(self.drawer_content_init()).start()
        home_tab.add_widget(self.drawer)

    def top_bar_init(self):

         # the drop down for the link box
        self.dropdown = MDDropdownMenu(width_mult=100)
        self.dropdown.background_color = get_sub_theme_color(essence="tuple")
        self.dropdown.position = "bottom"
        self.dropdown.border_margin = 0


        # the dropdown function
        def drop(instance, touch):
            if touch.button == "right":
                if self.nav_link.focus:
                    self.dropdown.open()
        # the top bar
        text_bx = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(40))

        self.nav_link = TextInput(size_hint=(1, 1), multiline=False)
        self.nav_link.background_active = ""
        self.nav_link.foreground_color = (1, 1, 1, 1)
        self.nav_link.background_normal = ""
        self.nav_link.font_name = "Assets/Fonts/Roboto-Light.ttf"
        self.nav_link.font_size = 18
        # self.nav_link.border = (10, 5, 5, 5)
        self.nav_link.hint_text = "Paste Link Here: Right click for more options"
        self.nav_link.on_text_validate = self.checker
         # menu items for the dropdown
        menu_items = [
            {
                "text": "Paste",
                "viewclass": "OneLineListItem",
                "on_release": lambda :self.copy_paste_empty(receiver="nav_link", action="paste")
            },
            {
                "text": "Cancel",
                "viewclass": "OneLineListItem",
                "on_release": lambda :self.copy_paste_empty(receiver="nav_link", action="empty")
            },
            {
                "text": "Copy",
                "viewclass": "OneLineListItem",
                "on_release": lambda :self.copy_paste_empty(receiver="nav_link", action="copy")
            },
            {
                "text": "Enter",
                "viewclass": "OneLineListItem",
                "on_release": self.checker
            }
        ]
        self.dropdown.items = menu_items

        text_bx.ids['nav_link'] = self.nav_link
        self.dropdown.caller = text_bx.ids.nav_link
        self.nav_link.bind(on_touch_down=drop)



        # the enter button
        self.enter_bt = Button(text="Enter", size_hint=(.1, 1), on_press=lambda obj: self.checker())
        self.enter_bt.background_normal = ""
        self.enter_bt.background_down = ""
        self.enter_bt.font_name = "Assets/Fonts/DroidSans.ttf"

        text_bx.add_widget(self.nav_link)
        text_bx.add_widget(self.enter_bt)
        self.home.add_widget(text_bx)

    def navbar_init(self):
        # the navigation bar
        self.navbar.add_widget(FlatButton(text="File", on_press=lambda obj: self.toggle_drawer()))
        self.download_popup()
        self.navbar.add_widget(FlatButton(text="Download", on_press=lambda obj: self.download_pop.pop()))

        self.navbar.add_widget(FlatButton(text="Settings", on_press=lambda obj: self.change_tab("settings")))
        self.navbar.add_widget(FlatButton(text="History", on_press=lambda obj: self.change_tab("history")))
        self.navbar.add_widget(FlatButton(text="Help", on_press=lambda obj: self.change_tab("help")))

    def info_bar_init(self):
        # the info bar
        infobar = MDCard(size_hint=(1, None), height=dp(20))
        self.home.add_widget(infobar)

        # the information
        infobar.add_widget(self.con_label)
        infobar.add_widget(self.down_label)
        infobar.add_widget(self.finished_label)
        infobar.add_widget(self.error_label)
        infobar.add_widget(self.paused_label)

    def drawer_content_init(self):
        # the sliding menu
        drawer_bg = BoxLayout(orientation="vertical")

        stats_box = BoxLayout(pos_hint={'top': 1}, size_hint=(1, .2), padding=(10, 10, 10, 10), spacing=(10, 10))

        downloads_box = BoxLayout()
        downloads_card = MDCard(size_hint=(1, 1), pos_hint={'x': 0, 'y': 0}, orientation="vertical", radius=5)
        downloads_card.md_bg_color = (.16, .55, 1, 1)
        downloads_card.add_widget(Label(pos_hint={'x': 0, 'y': .7}, height=dp(52), size_hint=(1, None), font_size=50,
                                        text=str(shorten_int(Config.total_downloads, 100, pd="99+"))))
        downloads_card.add_widget(Label(size_hint=(1, None), height=dp(25), text="Downloads"))
        downloads_box.add_widget(downloads_card)
        stats_box.add_widget(downloads_box)

        tab_a = Widget(size_hint=(.1, 1))
        stats_box.add_widget(tab_a)

        total_size_box = BoxLayout()
        total_size_card = MDCard(size_hint=(1, 1), pos_hint={'x': 0, 'y': 0})
        total_size_card.orientation = "vertical"
        total_size_card.radius = 5
        total_size_card.md_bg_color = (1, .4, .5, 1)
        total_size_card.add_widget(Label(pos_hint={'x': 0, 'y': .7}, height=dp(52), size_hint=(1, None), font_size=17,
                                         text=str(get_standard_size(Config.total_sizes))))
        total_size_card.add_widget(Label(size_hint=(1, None), height=dp(25), text="Total Size"))
        total_size_box.add_widget(total_size_card)
        stats_box.add_widget(total_size_box)

        tab_b = Widget(size_hint=(.1, 1))
        stats_box.add_widget(tab_b)

        total_speed_box = BoxLayout()
        total_speed_card = MDCard(size_hint=(1, 1), pos_hint={'x': 0, 'y': 0})
        total_speed_card.radius = 5
        total_speed_card.orientation = "vertical"
        total_speed_card.md_bg_color = (.5, 1, .4, 1)
        total_speed_card.add_widget(Label(pos_hint={'x': 0, 'y': .7}, height=dp(52), size_hint=(1, None), font_size=17,
                                          text=str(get_standard_size(Config.total_speeds)) + "/s"))
        total_speed_card.add_widget(Label(size_hint=(1, None), height=dp(25), text="Total Speed"))
        total_speed_box.add_widget(total_speed_card)
        stats_box.add_widget(total_speed_box)

        drawer_bg.add_widget(stats_box)

        button_box = BoxLayout(orientation="vertical", padding=(5, 10, 0, 5))

        inf_label = MDLabel(text="Categories")
        inf_label.color = (1, 1, 1, 1)
        inf_label.font_name = "Assets/Fonts/FiraCode-Bold.ttf"
        inf_label.font_size = dp(25)
        button_box.add_widget(inf_label)

        all_down = MDCard(size_hint=(1, 1))
        all_bt = Button(text="Show all downloads", on_press=lambda obj: self.change_download_tab("all"),
                        background_normal="", background_color="8F8D8A", on_release=lambda obj: self.toggle_drawer())

        all_down.add_widget(all_bt)
        button_box.add_widget(all_down)

        finished_down = MDCard(size_hint=(1, 1))
        fin_bt = Button(text="Show finished downloads", on_press=lambda obj: self.change_download_tab("finished"),
                        background_normal="", background_color="8F8D8A", on_release=lambda obj: self.toggle_drawer())

        finished_down.add_widget(fin_bt)
        button_box.add_widget(finished_down)

        down_down = MDCard(size_hint=(1, 1))
        down_bt = Button(text="Show downloading", on_press=lambda obj: self.change_download_tab("downloading"),
                         background_normal="", background_color="8F8D8A", on_release=lambda obj: self.toggle_drawer())

        down_down.add_widget(down_bt)
        button_box.add_widget(down_down)

        paused_down = MDCard(size_hint=(1, 1))
        paused_bt = Button(text="Show all paused downloads", on_press=lambda obj: self.change_download_tab("paused"),
                           background_normal="", background_color="8F8D8A", on_release=lambda obj: self.toggle_drawer())

        paused_down.add_widget(paused_bt)
        button_box.add_widget(paused_down)

        error_down = MDCard(size_hint=(1, 1))
        error_bt = Button(text="Show all Error downloads", on_press=lambda obj: self.change_download_tab("error"),
                          background_normal="", background_color="8F8D8A", on_release=lambda obj: self.toggle_drawer())

        error_down.add_widget(error_bt)
        button_box.add_widget(error_down)

        ess_label = MDLabel(text="Essentials")
        ess_label.color = (1, 1, 1, 1)
        ess_label.font_name = "Assets/Fonts/FiraCode-Bold.ttf"
        ess_label.font_size = dp(25)
        button_box.add_widget(ess_label)

        settings = MDCard()
        set_bt = Button(text="Change App Settings", on_press=lambda obj: self.toggle_drawer())
        set_bt.bind(on_press=lambda obj: self.change_tab("settings"))
        set_bt.background_normal = ""
        set_bt.background_color = "#3A9259"
        settings.add_widget(set_bt)
        button_box.add_widget(settings)

        history = MDCard()
        hist_bt = Button(text="Show Download Histories", on_press=lambda obj: self.toggle_drawer())
        hist_bt.bind(on_press=lambda obj: self.change_tab("history"))
        hist_bt.background_normal = ""
        hist_bt.background_color = "#FF9BA0"
        history.add_widget(hist_bt)
        button_box.add_widget(history)

        help_bt_card = MDCard()
        help_bt = Button(text="Find Help", on_press=lambda obj: self.change_tab("help"))
        help_bt.bind(on_press=lambda obj: self.toggle_drawer())

        help_bt.background_normal = ""
        help_bt.background_color = "#6AAFFF"
        help_bt_card.add_widget(help_bt)
        button_box.add_widget(help_bt_card)

        sys_bt_card = MDCard()
        sys_bt = Button(text="Exit App")
        sys_bt.background_normal = ""
        sys_bt.background_color = "#FF5356"
        sys_bt_card.add_widget(sys_bt)
        button_box.add_widget(sys_bt_card)

        drawer_bg.add_widget(button_box)

        inf_label = MDLabel(text="Information")
        inf_label.color = (1, 1, 1, 1)
        inf_label.font_name = "Assets/Fonts/FiraCode-Bold.ttf"
        inf_label.font_size = dp(25)
        button_box.add_widget(inf_label)

        sys_inf = PopupBox(essence="central", title="System Information",
                           bg_color=get_main_theme_color(essence="string"))
        sys_inf_box = BoxLayout(orientation="horizontal")
        sys_lbl_bx = BoxLayout(size_hint=(.45, 1), orientation='vertical')
        sys_lbl_bx.add_widget(MDLabel(text="Operating System"))
        sys_lbl_bx.add_widget(MDLabel(text="OS Version"))
        sys_lbl_bx.add_widget(MDLabel(text="System Architecture"))
        sys_lbl_bx.add_widget(MDLabel(text="System Processor"))
        sys_lbl_bx.add_widget(MDLabel(text="Machine"))
        sys_inf_box.add_widget(sys_lbl_bx)
        sys_cor_bx = BoxLayout(orientation="vertical")
        sys_cor_bx.add_widget(MDLabel(text=platform.system()))
        sys_cor_bx.add_widget(MDLabel(text=platform.version()))
        sys_cor_bx.add_widget(MDLabel(text=platform.architecture()[0]))
        sys_cor_bx.add_widget(MDLabel(text=platform.processor()))
        sys_cor_bx.add_widget(MDLabel(text=platform.machine()))
        sys_inf_box.add_widget(sys_cor_bx)

        sys_inf.content(sys_inf_box)

        sys_bt_card = MDCard()
        sys_bt = Button(text="System Information", on_press=lambda obj: sys_inf.pop())
        sys_bt.background_normal = ""
        sys_bt.background_color = "#FF5356"
        sys_bt_card.add_widget(sys_bt)
        button_box.add_widget(sys_bt_card)

        app_inf = PopupBox(essence="central", title="App Information", bg_color=get_main_theme_color(essence="string"))
        app_inf_box = BoxLayout(orientation="horizontal")
        app_lbl_bx = BoxLayout(size_hint=(.45, 1), orientation='vertical')
        app_lbl_bx.add_widget(MDLabel(text="App Version"))
        app_lbl_bx.add_widget(MDLabel(text="Product ID"))
        app_lbl_bx.add_widget(MDLabel(text="Last Update"))
        app_lbl_bx.add_widget(MDLabel(text="App Flavor"))
        app_lbl_bx.add_widget(MDLabel(text="App Release Date"))
        app_inf_box.add_widget(app_lbl_bx)
        app_cor_bx = BoxLayout(orientation="vertical")
        app_cor_bx.add_widget(MDLabel(text=Config.app_version))
        app_cor_bx.add_widget(MDLabel(text=Config.product_id))
        app_cor_bx.add_widget(MDLabel(text=Config.last_update))
        app_cor_bx.add_widget(MDLabel(text=str(Config.flavour)))
        app_cor_bx.add_widget(MDLabel(text=Config.release_date))
        app_inf_box.add_widget(app_cor_bx)
        app_inf.content(app_inf_box)

        app_bt_card = MDCard()
        app_bt = Button(text="App Information", on_press=lambda obj: app_inf.pop())
        app_bt.background_normal = ""
        app_bt.background_color = "#FF5356"
        app_bt_card.add_widget(app_bt)
        button_box.add_widget(app_bt_card)

        inf_card = MDCard()
        inf_card.size_hint = (1, None)
        inf_card.height = dp(100)
        inf_card.orientation = "vertical"
        lab = MDLabel(text="Geliana Software Incorporated")
        lab.font_size = 20
        lab_ad = MDLabel(text="Nairobi, Kenya")
        lab_rt = MDLabel(text="All Rights Reserved")
        lab_cr = MDLabel(text="Copyright @2021")
        lab_vs = MDLabel(text="Version " + str(Config.app_version))

        inf_card.add_widget(lab)
        inf_card.add_widget(lab_ad)
        inf_card.add_widget(lab_rt)
        inf_card.add_widget(lab_cr)
        inf_card.add_widget(lab_vs)

        button_box.add_widget(inf_card)

        self.drawer.add_widget(drawer_bg)

    def download_frame_init(self):
        self.home.add_widget(self.download_frame)

        self.download_frame.add_widget(self.download_frame_manager)

        self.all_downloads_tab.name = "all"
        self.download_frame_manager.add_widget(self.all_downloads_tab)

        self.init_download_tabs()

        self.downloading_tab.name = "downloading"
        self.download_frame_manager.add_widget(self.downloading_tab)

        self.paused_download_tab.name = "paused"
        self.download_frame_manager.add_widget(self.paused_download_tab)

        self.error_downloads_tab.name = "error"
        self.download_frame_manager.add_widget(self.error_downloads_tab)

        self.finished_downloads_tab.name = "finished"
        self.download_frame_manager.add_widget(self.finished_downloads_tab)

    def change_download_tab(self, tab):
        self.download_frame_manager.current = tab

    def toggle_drawer(self):
        self.drawer.set_state("toggle")

    def settings_tab_init(self):
        settings_tab = Screen(name="settings")
        self.manager.add_widget(settings_tab)

        self.back_st = Button(text="Back", on_press=lambda obj: self.change_tab("home"), size_hint=(None, None))
        self.back_st.background_normal = ""
        self.back_st.height = dp(50)
        self.back_st.width = dp(200)
        self.back_st.pos_hint = {'x': 0, 'y': .93}
        settings_tab.add_widget(self.back_st)

        settings_tab.add_widget(Image(source="Assets/Media/settings.png", size_hint=(None, None), height=dp(50),
                                      width=dp(50), pos_hint={'x': .21, "y": .93}))

        settings_tab.add_widget(
            Label(text="Settings", size_hint=(None, None), size=(dp(150), dp(50)), font_size=40, halign="left",
                  font_name="Assets/Fonts/Roboto-Light.ttf", pos_hint={"x": .265, "y": .93}))

        settings_tab.add_widget(
            Button(text="Restore Defaults", size_hint=(.2, None), height=dp(34), background_normal="",
                   background_color="04B5E6", pos_hint={'x': .45, 'y': .93},
                   on_press=lambda obj: restore_default_settings_query()))

        settings_tab.add_widget(
            Button(text="Cancel", size_hint=(.15, None), height=dp(35), background_color="FF5356", background_normal="",
                   pos_hint={'x': .68, 'y': .93}, on_press=lambda obj: cancel_new_settings()))

        settings_tab.add_widget(Button(text="Save", size_hint=(.15, None), height=dp(35), background_color="#3A9259",
                                       background_normal="", pos_hint={'x': .85, 'y': .93},
                                       on_press=lambda obj: save_new_settings_query()))

        self.settings_holder.size_hint = (1, .92)
        self.settings_holder.pos_hint = {"x": 0, "y": 0}

        settings_tab.add_widget(self.settings_holder)
        self.settings_holder.add_widget(settings_bg_scroll)

    def history_tab_init(self):
        # history_tab = Screen(name="history")
        # self.manager.add_widget(history_tab)
        
        # top = BoxLayout(size_hint=(1, .05), pos_hint={'x': 0, 'y': .93}, orientation="vertical")
        
       
        # self.history_holder.orientation = "vertical"
        # history_tab.add_widget(top)
        
        # bottom = BoxLayout(size_hint=(1, .92), orientation="vertical")
        # stroller = ScrollView()
        # stroller.bar_color = "298AFF"
        # stroller.bar_width = 5
        # stroller.do_scroll_y = True
        # self.history_holder = BoxLayout(size_hint=(1, None), orientation="vertical")

        # stroller.add_widget(self.history_holder)
        # bottom.add_widget(stroller)
        # history_tab.add_widget(bottom)
        history = Screen(name="history")

        top = BoxLayout(size_hint=(1, .05), pos_hint={'x': 0, 'y': .93})

        self.back_hst = Button(text="Back", on_press=lambda obj: multiprocessing.Process(self.change_tab("home")).start, size_hint=(None, None))
        self.back_hst.background_normal = ""
        self.back_hst.height = dp(50)
        self.back_hst.width = dp(200)
        #self.back_hst.pos_hint = {'x': 0, 'y': .93}
        top.add_widget(self.back_hst)

        top.add_widget(Image(source="Assets/Media/history.png", size_hint=(None, None), height=dp(50),
                                     width=dp(50)))

        top.add_widget(
            Label(text="History", size_hint=(None, None), size=(dp(150), dp(50)), font_size=40, halign="left",
                  font_name="Assets/Fonts/Roboto-Light.ttf"))

        top.add_widget(Widget())
        top.add_widget(
            Button(text="Clear All Histories", size_hint=(None, None), background_normal="", background_down="", background_color="FF5356",
                   height=dp(50), width=dp(250), pos_hint={'x': .45, 'y': 0}, on_press=lambda obj: threading.Thread(delete_it).start())
        )
       

        def deleting_download(obj):
            str(obj)
            print(p.StorageAPI().get_all_pids())
            for pid in p.StorageAPI().get_all_pids():
                self.history_holder.remove_widget(self.history_holder.ids[str(pid)])

            p.StorageAPI().delete_all_data()
            SnackBar(essence="extra", message="Record Deleted", bg_color=get_sub_theme_color(essence="tuple"))

        def delete_it():
            if not p.KeyMatch().match("save_down_proc"):
                deleting_download(obj=None)
            elif p.KeyMatch().match("save_down_proc"):
                box = PopupBox(essence="central", title="Cancel Download",
                               bg_color=get_sub_theme_color(essence="string"),
                               escape=False)

                def leave(obj):
                    str(obj)
                    box.exit()
        

        bottom = BoxLayout(size_hint=(1, .92))
        stroller = ScrollView()
        stroller.bar_color = "298AFF"
        stroller.bar_width = 5
        stroller.do_scroll_y = True
        self.history_holder = BoxLayout(size_hint=(1, None), orientation="vertical")

        def hst():
            for i in p.StorageAPI().get_all_ids():
                self.history_tabs(i)
        threading.Thread(target=lambda: hst()).start()
       
       
        history.add_widget(top)
        history.add_widget(bottom)
        bottom.add_widget(stroller)
        stroller.add_widget(self.history_holder)
        
        self.manager.add_widget(history)

        def update_history(delta_time):
            
            self.history_holder.height = len(p.StorageAPI().get_all_ids()) * 100

        Clock.schedule_interval(update_history, 1 / 99999999999)

    def open_help(self, obj):
        str(obj)
        self.manager.current = "help"
        SnackBar(essence="extra", message="Help", bg_color=get_sub_theme_color(essence="tuple"))

    def open_history(self, obj):
        str(obj)
        self.manager.current = "history"
        SnackBar(essence="extra", message="History", bg_color=get_sub_theme_color(essence="tuple"))

    def error_downloads_screen_content(self):
        holder_bx = BoxLayout(orientation="vertical")
        down_box = BoxLayout(size_hint=(1, .07))

        # the Label
        down_info_label = MDLabel(text="Error Downloads", font_name="Assets/fonts/FiraCode-Bold.ttf", size_hint=(.3, 1),
                                  pos_hint={'x': .2, 'y': 0})
        down_box.add_widget(down_info_label)
        down_info_label.color = (1, 1, 1, 1)
        down_info_label.font_size = dp(25)

        down_info_no_label = MDLabel(text="0", font_name="Assets/fonts/FiraCode-Bold.ttf", size_hint=(.1, 1))
        down_box.add_widget(down_info_no_label)
        down_info_no_label.color = (1, 1, 1, 1)
        down_info_no_label.font_size = dp(15)

        left = MDIconButton(icon="arrow-left-bold-hexagon-outline", on_press=self.open_finished_download_screen)

        down_box.add_widget(left)

        holder_bx.add_widget(down_box)

        scroll_all = ScrollView()
        scroll_all.bar_color = "298AFF"
        scroll_all.bar_width = 5
        scroll_all.do_scroll_y = True

        self.error_downloads_box = BoxLayout(orientation="vertical", size_hint=(1, None))

        # adding widgets
        self.error_downloads_screen.add_widget(holder_bx)
        holder_bx.add_widget(scroll_all)
        scroll_all.add_widget(self.error_downloads_box)

        def mini_update(delta_t):
            str(delta_t)
            down_info_no_label.text = str(self.errors)

        Clock.schedule_interval(mini_update, 1 / 99999999999)

    def help_tab_init(self):
        help_tab = Screen(name="help")
        self.manager.add_widget(help_tab)

        self.back_hp = Button(text="Back", on_press=lambda obj: multiprocessing.Process(self.change_tab("home")).start(), size_hint=(None, None))
     
        self.back_hp.background_normal = ""
        self.back_hp.height = dp(50)
        self.back_hp.width = dp(200)
        self.back_hp.pos_hint = {'x': 0, 'y': .93}
        help_tab.add_widget(self.back_hp)

        help_tab.add_widget(Image(source="Assets/Media/help.png", size_hint=(None, None), height=dp(50),
                                  width=dp(50), pos_hint={'x': .21, "y": .93}))

        help_tab.add_widget(
            Label(text="Help", size_hint=(None, None), size=(dp(150), dp(50)), font_size=40, halign="left",
                  font_name="Assets/Fonts/Roboto-Light.ttf", pos_hint={"x": .25, "y": .93}))

    def change_tab(self, tab):
        if tab == "home":
            if not affirm_settings():
                save_new_settings_query()
            elif affirm_settings():
                self.manager.current = tab
        elif tab == "history":
            self.manager.current = tab

        else:
            self.manager.current = tab

    def app_essentials_update(self, delta_t):
        str(delta_t)

        """The customized tabs labels that show the stats"""
        all_label.text = str(self.downloads + self.errors + self.paused + self.finished)
        downloading_label.text = str(self.downloads)
        paused_label.text = str(self.paused)
        error_label.text = str(self.errors)
        finished_label.text = str(self.finished)

        # update the downloads box in the mini-tabs
        all_downloads_box.height = self.downloads * 100
        
        # themes and colors
        self.theme = get_main_theme_color(essence="tuple")
        self.drawer.md_bg_color = get_main_theme_color(essence="tuple")
        self.enter_bt.background_color = get_sub_theme_color(essence="string")
        self.nav_link.background_color = get_transparent_sub_theme_color(essence="string")
        self.nav_link.hint_text_color = "#FFFFFF"
        self.back_st.background_color = get_transparent_sub_theme_color(essence="string")
        self.back_hst.background_color = get_transparent_sub_theme_color(essence="string")
        self.back_hp.background_color = get_transparent_sub_theme_color(essence="string")

        # info bar statistics

        # checking for internet connection
        if check_network_connection():
            self.con_label.text = "Internet connected"
            self.con_label.color = "#298AFF"
        else:
            self.con_label.text = "No Connection"
            self.con_label.color = "#FF0500"

        # check for any errors encountered
        if self.errors == 1:
            self.error_label.color = "#FF0500"
            self.error_label.text = str(self.errors) + " Error"
        elif self.errors > 1:
            self.error_label.color = "#FF0500"
            self.error_label.text = str(self.errors) + " Errors"
        elif self.errors < 1:
            self.error_label.color = "#00920F"
            self.error_label.text = "No errors"

        # check for any finished procedures
        if self.finished > 0:
            self.finished_label.text = str(self.finished) + " Finished"
            self.finished_label.color = "#298AFF"
        elif self.finished == 0:
            self.finished_label.color = "#00920F"
            self.finished_label.text = "None Finished"

        # check for any downloading procedures
        if self.downloads > 0:
            self.down_label.text = str(self.downloads) + " Downloading.."
            self.down_label.color = "#298AFF"
        elif self.downloads == 0:
            self.down_label.text = "None Downloading"
            self.down_label.color = "#00920F"

        # check for any paused downloads
        if self.paused > 0:
            self.paused_label.text = str(self.paused) + " Paused"
            self.paused_label.color = "#298AFF"
        elif self.paused == 0:
            self.paused_label.color = "#00920F"
            self.paused_label.text = "None Paused"

    def download_popup(self):
        self.download_pop = PopupBox(essence="central", title="Input URL", bg_color=get_sub_theme_color("string"),
                                     escape=False)

        download_inner = FloatLayout()
        download_inner.add_widget(Label(text="Link", size_hint=(None, None), height=dp(25), width=dp(25),
                                        pos_hint={'x': 0, 'y': .75}))

        self.url_box = MDTextField(mode="rectangle", hint_text="Paste url here", multiline=False)
        self.url_box.background_disabled_normal = ""
        self.url_box.font_name = "Assets/Fonts/JetBrainsMono-Thin.ttf"
        self.url_box.background_color = '#BECAFF'
        self.url_box.background_normal = ""
        self.url_box.size_hint = (.6, .2)
        self.url_box.pos_hint = {'x': .2, 'y': .75}

        self.url_box.on_text_validate = self.download_pop.exit
        self.url_box.on_text_validate = self.checker

        download_inner.add_widget(
            Button(text="Paste", size_hint=(None, None), height=dp(30), width=dp(70), pos_hint={'x': .85, 'y': .75},
                   on_press=lambda obj: self.copy_paste_empty(receiver="url_box", action="paste")))

        download_inner.add_widget(self.url_box)

        download_inner.add_widget(
            Label(text="Directory", size_hint=(None, None), height=dp(25), width=dp(25), pos_hint={'x': .03, 'y': .45}))

        self.dir_input = MDTextField(text=p.KeyMatch().match("directory"))
        self.dir_input.mode = "rectangle"
        self.dir_input.hint_text = "directory"
        self.dir_input.multiline = False
        self.dir_input.background_normal = ""
        self.dir_input.size_hint = (.6, .2)

        download_inner.add_widget(
            Button(text="Change", size_hint=(None, None), pos_hint={'x': .85, 'y': .45}, height=dp(30),
                   width=dp(70), on_press=lambda obj: self.change_directory()))

        self.dir_input.pos_hint = {'x': .2, 'y': .45}
        download_inner.add_widget(self.dir_input)

        download_inner.add_widget(
            Button(text="Cancel", on_press=lambda obj: self.download_pop.exit(), background_normal="",
                   background_color="#FF5356", size_hint=(None, None), height=dp(25), pos_hint={'x': 0, 'y': 0},
                   on_release=lambda obj: self.copy_paste_empty("url_box", action="empty")))

        download_enter = Button(on_press=lambda obj: self.download_pop.exit(), text="Proceed",
                                background_color="#0976FF", size_hint=(None, None), background_normal="", height=dp(25),
                                pos_hint={'x': .79, 'y': 0})
        download_enter.bind(on_press=lambda obj: self.checker())
        download_inner.add_widget(download_enter)
        self.download_pop.content(content=download_inner)

    def copy_paste_empty(self, receiver, action):
        if receiver == "nav_link":
            if action == "paste":
                self.nav_link.text = paste_data()
            elif action == "copy":
                copy_data(self.nav_link.text)
            elif action == "empty":
                self.nav_link.text = ""
        elif receiver == "url_box":
            if action == "paste":
                self.url_box.text = paste_data()
            elif action == "copy":
                copy_data(self.url_box.text)
            elif action == "empty":
                self.url_box.text = ""

    def change_directory(self):
        root = tk.Tk()
        root.iconbitmap("Assets/Media/downloader.ico")
        root.withdraw()
        folder = filedialog.askdirectory()
        if folder == "" or folder is None:
            self.dir_input.text = p.KeyMatch().match("directory")
            SnackBar(essence="info", message="Directory reverted to original", bg_color=get_main_theme_color("tuple"))

        else:
            self.dir_input.text = folder
            SnackBar(essence="info", message="Directory changed", bg_color=get_main_theme_color("tuple"))

    def checker(self):
        # this checker is used to look for the actual url where it has been placed either in the nav_link textinput or in the download popup
        #it also checks for empty input from both textinputs, internet connection and url validity

        importlib.reload(p)
        #Refresh the preferences
        if not self.nav_link.text and not self.url_box.text:
            PopupBox(essence="warn", error_code="URL345", message="Failure: No URL was encountered", beep=True).pop()
        elif not check_network_connection(use="external"):
            PopupBox(essence="warn", error_code="NT101", message="Failure: No Internet Connection", beep=True).pop()

        else:
            if self.nav_link.text:

                if not check_link_validity(url=self.nav_link.text, use="external"):
                    PopupBox(essence="warn", error_code="URL201", message="Failure: Invalid URL",
                             beep=True).pop()
                    self.nav_link.text = ""
                else:
                    self.confirmer(self.nav_link.text, p.KeyMatch().match("directory"))
                    self.nav_link.text = ""

            elif self.url_box.text:
                if not check_link_validity(url=self.url_box.text, use="external"):
                    PopupBox(essence="warn", error_code="URL202", message="Failure: Invalid URL",
                             beep=True).pop()
                    self.url_box.text = ""
                else:
                    self.confirmer(self.url_box.text, self.dir_input.text)
                    self.url_box.text = ""

    def confirmer(self, url, place):
        tag = create_random_characters()
        identifier = create_random_characters()
        pid = create_random_characters()

        thread = TellyEngine(url=url, directory=place, tag=tag, identifier=identifier, process_id=pid)
        if p.KeyMatch().match("approval"):

            affirm = PopupBox(essence="central", title="Approve Download",
                              bg_color=get_sub_theme_color(essence="string"),
                              escape=False)

            background = BoxLayout(orientation="vertical")

            top = BoxLayout()
            stat_box = BoxLayout(size_hint=(.75, 1), orientation="vertical")

            name_box = BoxLayout()
            file_name_label = MDLabel(text="Name: ", size_hint=(.3, 1))
            file_name = MDLabel(text="Waiting....")

            dir_box = BoxLayout()
            dir_name_label = MDLabel(text="Directory: ", size_hint=(.3, 1))
            dir_name = MDLabel(text=shorten_string(place, 37))
            dir_name.color = "E0E3E6"

            link_box = BoxLayout()

            link_name_label = MDLabel(text="Link: ", size_hint=(.3, 1))
            link_name = MDLabel(text=shorten_string(url, 37))
            link_name.color = "E0E3E6"

            size_box = BoxLayout()
            link_size_label = MDLabel(text="Size: ", size_hint=(.3, 1))
            link_size = MDLabel(text="Waiting")
            link_size.color = "E0E3E6"

            info_box = BoxLayout(size_hint=(.25, 1), orientation="vertical")

            pic_box = BoxLayout()
            file_icon = Image(size_hint=(.6, .6), pos_hint={'x': 0, 'y': .2})

            media_type_box = BoxLayout(size_hint=(1, .3))
            media_type_label = Label(text="Waiting....", size_hint=(1, 1))

            bottom = BoxLayout(size_hint=(1, .3))
            c_cancel = Button(text="Cancel", on_press=lambda obj: affirm.exit(), size_hint=(None, None), height=dp(30),
                              background_normal="")
            c_cancel.background_color = "#FF5356"
            c_proceed = Button(text="Proceed",
                               on_press=lambda obj: self.init_download(sequence=thread),
                               size_hint=(None, None),
                               background_normal="", on_release=lambda obj: affirm.exit())
            c_proceed.background_color = "#0976FF"
            c_proceed.pos_hint = {'x': .8, 'y': 0}
            c_proceed.height = dp(30)

            def get_essentials():
                file_name.text = shorten_string(thread.get_name(), 37)
                file_name.color = "E0E3E6"
                link_size.text = str(get_standard_size(int(thread.get_size())))
                link_size.color = "E0E3E6"
                media_type_label.text = thread.get_media()
                media_type_label.color = "E0E3E6"

            def get_icon():
                file_icon.source = check_type(thread.get_media(), thread.get_file_extension())

            get_icon()

            def update(delta):
                str(delta)
                threading.Thread(target=lambda: get_essentials()).start()

            Clock.schedule_interval(update, 1 / 999999999999)
            background.add_widget(top)
            top.add_widget(stat_box)
            name_box.add_widget(file_name_label)
            name_box.add_widget(file_name)
            dir_box.add_widget(dir_name_label)
            dir_box.add_widget(dir_name)
            link_box.add_widget(link_name_label)
            link_box.add_widget(link_name)
            stat_box.add_widget(name_box)
            stat_box.add_widget(dir_box)
            stat_box.add_widget(link_box)
            stat_box.add_widget(size_box)
            size_box.add_widget(link_size_label)
            size_box.add_widget(link_size)
            top.add_widget(info_box)
            info_box.add_widget(pic_box)
            pic_box.add_widget(file_icon)
            info_box.add_widget(media_type_box)
            media_type_box.add_widget(media_type_label)
            background.add_widget(bottom)
            bottom.add_widget(c_cancel)
            bottom.add_widget(Widget())
            bottom.add_widget(c_proceed)

            affirm.pop()
            affirm.content(content=background)
        elif not p.KeyMatch().match("approval"):
            self.init_download(sequence=thread)

    def init_download(self, sequence):
        if sequence.confirm_existence():
            self.add_download_tab("all", sequence)
        elif not sequence.confirm_existence():
            PopupBox(essence="warn", title="Error Sequence", error_code="SEQ124", message="invalid sequence").pop()

    def add_download_tab(self, receiver, sequence):

        if receiver == "all":
            open(sequence.get_file_location_name(), "w")
            self.start_download(sequence)
            all_downloads_box.add_widget(self.all_downloads_downloading_tab(sequence), index=self.downloads - 1)

    def start_download(self, sequence):
        SnackBar(essence="info", message="Download Started", bg_color=get_main_theme_color("tuple"))
        self.downloads += 1
        today_date = dt.date.today()
        time_now = dt.datetime.now()
        self.in_service_pids.append(sequence.get_process_identifier())
        detail = {'id': sequence.get_identifier(),
                  'tag': sequence.get_tag(),
                  'pid': sequence.get_process_identifier(),
                  'url': sequence.get_url(),
                  'name': sequence.get_name(),
                  'size': sequence.get_size(),
                  'media': sequence.get_media(),
                  'secondary_location': "downloading_screen",
                  'directory': sequence.get_directory(),
                  'timestamp': {'start_date': f"{today_date:%A, %B %d, %Y}", 'start_time': f"{time_now: %I:%M %p}",
                                'finish_date': "", 'finish_time': ""}}
        p.StorageAPI().add_data(detail)
        sequence.download_file()

    def init_download_tabs(self):
        self.all_downloads_tab.add_widget(all_downloads_bg)
        all_paused.bind(on_press=lambda obj: self.change_download_tab("paused"))
        all_downloading.bind(on_press=lambda obj: self.change_download_tab("downloading"))
        all_finished.bind(on_press=lambda obj: self.change_download_tab("finished"))
        all_error.bind(on_press=lambda obj: self.change_download_tab("error"))

        self.downloading_tab.add_widget(downloading_bg)
        downloading_all.bind(on_press=lambda obj: self.change_download_tab("all"))
        downloading_paused.bind(on_press=lambda obj: self.change_download_tab("paused"))
        downloading_finished.bind(on_press=lambda obj: self.change_download_tab("finished"))
        downloading_error.bind(on_press=lambda obj: self.change_download_tab("error"))

        self.paused_download_tab.add_widget(paused_bg)
        paused_all.bind(on_press=lambda obj: self.change_download_tab("all"))
        paused_downloading.bind(on_press=lambda obj: self.change_download_tab("downloading"))
        paused_finished.bind(on_press=lambda obj: self.change_download_tab("finished"))
        paused_error.bind(on_press=lambda obj: self.change_download_tab("error"))

        self.error_downloads_tab.add_widget(error_bg)
        error_all.bind(on_press=lambda obj: self.change_download_tab("all"))
        error_downloading.bind(on_press=lambda obj: self.change_download_tab("downloading"))
        error_finished.bind(on_press=lambda obj: self.change_download_tab("finished"))
        error_paused.bind(on_press=lambda obj: self.change_download_tab("paused"))

        self.finished_downloads_tab.add_widget(finished_bg)
        finished_all.bind(on_press=lambda obj: self.change_download_tab("all"))
        finished_downloading.bind(on_press=lambda obj: self.change_download_tab("downloading"))
        finished_error.bind(on_press=lambda obj: self.change_download_tab("error"))
        finished_paused.bind(on_press=lambda obj: self.change_download_tab("paused"))

    def all_downloads_downloading_tab(self, sequence):
        # Downloadtab styling
        downloadtab = BoxLayout(orientation="horizontal", )
        all_downloads_box.ids[sequence.get_tag()] = downloadtab
        downloadtab.spacing = (dp(5), dp(5))
        downloadtab.padding = (dp(3), dp(3), dp(3), dp(3))
        downloadtab.pos_hint = {'x': 0, 'y': 1}
        downloadtab.center_x = 0
        downloadtab.size_hint = (1, None)
        downloadtab.height = dp(100)

        down_bg = MDCard(elevation=15)
        down_bg.radius = 0

        media_box = BoxLayout(orientation="vertical", size_hint=(.15, 1))
        icon_box = BoxLayout(size_hint=(1, .7))

        file_icon = Image(source=check_type(sequence.get_media(), sequence.get_file_extension()), size_hint=(.8, .8),
                          pos_hint={'x': .1, 'y': .1})

        media_type_box = BoxLayout(size_hint=(1, .3))
        media_type_label = Label(text=sequence.get_media(), size_hint=(1, 1))

        info_box = BoxLayout(orientation="vertical", size_hint=(.8, 1))

        name_label = MDLabel(text="Waiting...")
        name_label.color = "E0E3E6"

        direc_label = MDLabel(text=sequence.get_directory())
        direc_label.color = "E0E3E6"

        progress = MDProgressBar(value=0, max=100, size_hint=(1, .25))

        stat_box = BoxLayout(orientation="horizontal")

        state_label = MDLabel(text="State: Waiting...", size_hint=(.4, 1))
        state_label.color = "E0E3E6"

        size_label = Label(text="Size: -- / --", size_hint=(.4, 1), font_name="Assets/Fonts/Lcd.ttf")

        speed_label = Label(text="speed: 0mbps", size_hint=(.2, 1), font_name="Assets/Fonts/Lcd.ttf", bold=True)

        eta_label = Label(text="4s left", size_hint=(.2, 1))

        percent_box = BoxLayout(size_hint=(.05, 1))

        percent_label = Label(text="-- %", size_hint=(.05, 1), font_name="Assets/Fonts/Lcd.ttf", bold=True)

        button_box = BoxLayout(orientation="vertical", size_hint=(.1, 1))

        pause = Button(text="pause")
        cancel_bt = Button(text="cancel")

        # adding the  widgets declared above
        downloadtab.add_widget(down_bg)
        down_bg.add_widget(media_box)
        media_box.add_widget(icon_box)
        icon_box.add_widget(file_icon)
        media_box.add_widget(media_type_box)
        media_type_box.add_widget(media_type_label)
        down_bg.add_widget(info_box)
        info_box.add_widget(name_label)
        info_box.add_widget(direc_label)
        info_box.add_widget(progress)
        info_box.add_widget(stat_box)
        stat_box.add_widget(state_label)
        stat_box.add_widget(size_label)
        stat_box.add_widget(speed_label)
        stat_box.add_widget(eta_label)
        down_bg.add_widget(percent_box)
        percent_box.add_widget(percent_label)
        down_bg.add_widget(button_box)
        button_box.add_widget(pause)
        button_box.add_widget(cancel_bt)

        speed_time = 0
        down_finish = False
        down_pause = False

        def update_tab(delta):
            nonlocal speed_time
            nonlocal down_finish
            nonlocal down_pause
            down_bg.md_bg_color = get_sub_theme_color("tuple")
            name_label.text = sequence.get_name()
            progress.color = (1, 1, 1, 1)
            if not check_network_connection(use="internal"):
                state_label.text = "State: Network Error"
                state_label.color = "#FF0500"
                speed_label.text = "- - bytes/s"
            elif check_network_connection(use="internal"):

                if os.path.getsize(sequence.get_file_location_name()) == sequence.get_size():
                    state_label.text = "State: Finished"
                    cancel_bt.on_press = lambda obj: do_nothing()
                    state_label.color = "#00DFFF"
                    pause.on_press = lambda obj: do_nothing()
                    cancel_bt.icon = "check"
                    pause.icon = "check"
                    progress.value = 100
                    percent_label.text = "100 %"
                    size_label.text = str(
                        get_standard_size(sequence.get_size()) + "/" + get_standard_size(sequence.get_size()))
                    state_label.color = "#00DFFF"
                    speed_label.text = "- - bytes/s"
                    if not down_finish:
                        self.finished_download(sequence.get_identifier())
                        down_finish = True

                elif not os.path.getsize(sequence.get_file_location_name()) == sequence.get_size():
                    if not os.path.exists(sequence.get_error_file()):
                        state_label.text = "State: Downloading"
                        state_label.color = "#FFFFFF"
                        pause.on_press = lambda obj: self.pause_download(sequence.get_identifier(),
                                                                         sequence.get_error_file())
                        progress.value = (int(
                            os.path.getsize(sequence.get_file_location_name())) / int(sequence.get_size())) * 100
                        percent_label.text = str(int(progress.value)) + " %"
                        size_label.text = str(
                            get_standard_size(os.path.getsize(sequence.get_file_location_name()))) + "/ " + str(
                            get_standard_size(int(sequence.get_size())))
                        down_pause = False
                        speed_time += delta
                        speed_label.text = str(get_standard_size(sequence.get_size() / speed_time)) + "/s"
                    elif os.path.exists(sequence.get_error_file()):
                        state_label.text = "State: Paused"
                        cancel_bt.on_press = lambda obj: do_nothing()
                        pause.on_press = lambda obj: self.resume_download(sequence)
                        state_label.color = "#00DFFF"
                        cancel_bt.disabled = True
                        pause.text = "Resume"
                        if not down_pause:
                            down_pause = True
                            self.pause_download(sequence.get_identifier(), sequence.get_error_file())

        Clock.schedule_interval(update_tab, 1 / 99)

        return downloadtab

    def pause_download(self, identifier, error_file):
        SnackBar(essence="info", message="Download Paused", bg_color=get_main_theme_color("tuple"))
        self.downloads -= 1
        self.paused += 1
        pid = p.StorageAPI().get_unknown(identifier, "pid")
        if pid in self.in_service_pids:
            self.in_service_pids.pop(self.in_service_pids.index(pid))
        if not os.path.exists(error_file):
            open(error_file, "w")

    def finished_download(self, identifier):
        SnackBar(essence="info", message="Download Completed", bg_color=get_main_theme_color("tuple"))
        self.downloads -= 1
        self.finished += 1
        process_id = p.StorageAPI().get_unknown(identifier, "pid")
        self.in_service_pids.pop(self.in_service_pids.index(process_id))

        if p.KeyMatch().match("beep_finish"):
            threading.Thread(target=lambda: beep()).start()
        else:
            pass

    def resume_download(self, sequence):
        SnackBar(essence="info", message="Download Resumed", bg_color=get_main_theme_color("tuple"))
        self.paused -= 1
        self.downloads += 1
        sequence.resume_download()
        if os.path.exists(sequence.get_error_file()):
            os.remove(sequence.get_error_file())

    def populate_history(self):
        for i in p.StorageAPI().get_all_ids():
            self.history_tabs(i)
    
    def history_tabs(self, identifier):
        history_tab = BoxLayout()
        history_tab.spacing = (dp(5), dp(5))
        history_tab.padding = (dp(3), dp(3), dp(3), dp(3))
        history_tab.center_x = 0
        history_tab.size_hint = (1, None)
        history_tab.height = dp(100)
        pid = p.StorageAPI().get_unknown(identifier, "pid")
        self.history_holder.ids[pid] = history_tab

        down_bg = MDCard(elevation=15)
        down_bg.radius = 0

        info_box = BoxLayout(orientation="vertical")

        name = p.StorageAPI().get_unknown(identifier, "name")
        name_label = MDLabel(text=name)
        name_label.color = "E0E3E6"

        direc_label = MDLabel(text=p.StorageAPI().get_unknown(identifier, "directory"))
        direc_label.color = "E0E3E6"

        progress = MDLabel(text=shorten_string(p.StorageAPI().get_unknown(identifier, "url"), 100))

        stat_box = BoxLayout(orientation="horizontal")

        state_label = MDLabel(text=shorten_string(str(p.StorageAPI().get_unknown(identifier, "media")), 14), size_hint=(.1, 1))
        state_label.color = "E0E3E6"

        size_label = MDLabel(
            text=str(get_standard_size(p.StorageAPI().get_unknown(identifier, "size"))),
            size_hint=(.1, 1))
        size_label.font_name = "Assets/Fonts/Lcd.ttf"

        a = str(p.StorageAPI().get_unknown(identifier, "timestamp")["start_date"]) + str(
            p.StorageAPI().get_unknown(identifier, "timestamp")["start_time"])

        speed_label = MDLabel(text="Started at:" + a, size_hint=(.35, 1))

        eta_label = MDLabel(
            text="Finished at:" + str(p.StorageAPI().get_unknown(identifier, "timestamp")["finish_date"] + str(
                p.StorageAPI().get_unknown(identifier, "timestamp")["finish_time"])),
            size_hint=(.35, 1))

        def copy_url():
            data = p.StorageAPI().get_unknown(identifier, "url")
            copy_data(data)
            SnackBar(essence="info", message="Link has been copied.", bg_color=get_sub_theme_color(essence="tuple"))

        def deleting_download(obj):
            str(obj)
            self.history_holder.remove_widget(self.history_holder.ids[pid])
            p.StorageAPI().delete_data(identifier)
            SnackBar(essence="extra", message="Record Deleted", bg_color=get_sub_theme_color(essence="tuple"))
            threading.Thread(self.history_holder.clear_widgets()).start()
            threading.Thread(self.populate_history()).start()
            
            
        def delete_it():
            if not p.KeyMatch().match("save_down_proc"):
                deleting_download(obj=None)
            elif p.KeyMatch().match("save_down_proc"):
                box = PopupBox(essence="central", title="Cancel Download",
                               bg_color=get_sub_theme_color(essence="string"),
                               escape=False)

                def leave(obj):
                    str(obj)
                    box.exit()

                bg_back = BoxLayout(orientation="vertical")
                bg_label = Label(text="Are You Sure to Delete records to this download?")
                bg_back.add_widget(bg_label)
                btn_box = BoxLayout(size_hint=(1, .3))
                proc_bt = Button(text="Proceed", on_press=deleting_download, on_release=leave)
                canc_bt = Button(text="Cancel", on_press=leave)
                btn_box.add_widget(proc_bt)
                btn_box.add_widget(canc_bt)
                bg_back.add_widget(btn_box)

                box.pop()
                box.content(bg_back)
        

        bt_box = BoxLayout(size_hint=(.04, 1), orientation="vertical")

        url_paste = MDIconButton(icon="content-copy")
        url_paste.on_press = copy_url
        del_bt = MDIconButton(icon="delete")
        del_bt.on_press = delete_it

        # adding the  widgets declared above
        down_bg.add_widget(info_box)
        info_box.add_widget(name_label)
        info_box.add_widget(direc_label)
        info_box.add_widget(progress)
        info_box.add_widget(stat_box)
        stat_box.add_widget(state_label)
        stat_box.add_widget(size_label)
        stat_box.add_widget(speed_label)
        stat_box.add_widget(eta_label)
        down_bg.add_widget(bt_box)
        bt_box.add_widget(url_paste)
        bt_box.add_widget(del_bt)
        history_tab.add_widget(down_bg)
        self.history_holder.add_widget(history_tab)

        def update_tab(delta_time):
            str(delta_time)
            down_bg.md_bg_color = get_sub_theme_color("tuple")

        Clock.schedule_interval(update_tab, 1 / 9999)


class MainApp(MDApp):
    def build(self):
        self.title = "Telly Download Manager"
        return MainLayout()


if __name__ == "__main__":
    MainApp().run()
