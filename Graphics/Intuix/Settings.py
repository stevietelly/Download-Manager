from Graphics.Card import Card
from Graphics.Intuix.set_tabs import all_settings_tab, int_switch, valid_switch, conc_input, approve_switch, dir_input, \
    warn_switch, theme_input, notifications_switch, ask_switch, download_save_switch, beep_finish_switch, \
    beep_error_switch
import Assets.Functions.Parser as p
from Graphics.Colors import get_main_theme_color, get_sub_theme_color
from Graphics.Popups import PopupBox, SnackBar

from kivy.metrics import dp
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget

import importlib

settings_bg_scroll = ScrollView(size_hint=(1, 1))
settings_bg_scroll.bar_color = "298AFF"
settings_bg_scroll.bar_width = 5
settings_bg_scroll.do_scroll_y = True

settings_bg = BoxLayout(orientation="vertical")
settings_bg.padding = (5, 5, 5, 5)
settings_bg.spacing = (10, 10)
settings_bg.size_hint = (1, None)
settings_bg.height = 0


def add_settings_tab(widget):
    settings_bg.height += dp(50)
    card = Card()
    card.add_widget(widget)
    settings_bg.add_widget(card)

    settings_bg.add_widget(Widget(size_hint=(1, None), height=dp(10), pos_hint={"x": 0, "y": 1}))


settings_bg_scroll.add_widget(settings_bg)

for i in all_settings_tab:
    add_settings_tab(i)


def affirm_settings():
    original = {'preferences': [
        {'setting': ['internet_validation'],
         'value': [p.KeyMatch().match("internet_validation")]},
        {'setting': ['link_validation'],
         'value': [p.KeyMatch().match("link_validation")]},
        {'setting': ['concurrency_limit'],
         'value': [int(p.KeyMatch().match("concurrency_limit"))]},
        {'setting': ['approval'],
         'value': [p.KeyMatch().match("approval")]},
        {'setting': ['directory'],
         'value': [str(p.KeyMatch().match("directory"))]},
        {'setting': ['warning'],
         'value': [p.KeyMatch().match("warning")]},
        {'setting': ['theme'],
         'value': [str(p.KeyMatch().match("theme"))]},
        {'setting': ['notifications'],
         'value': [p.KeyMatch().match("notifications")]},
        {'setting': ['warn_settings'],
         'value': [p.KeyMatch().match("warn_settings")]},
        {'setting': ['save_down_proc'],
         'value': [p.KeyMatch().match("save_down_proc")]},
        {'setting': ['beep_finish'],
         'value': [p.KeyMatch().match("beep_finish")]},
        {'setting': ['beep_error'],
         'value': [p.KeyMatch().match("beep_error")]}
    ]}
    now_values = {'preferences': [
        {'setting': ['internet_validation'],
         'value': [int_switch.active]},
        {'setting': ['link_validation'],
         'value': [valid_switch.active]},
        {'setting': ['concurrency_limit'],
         'value': [int(conc_input.text)]},
        {'setting': ['approval'],
         'value': [approve_switch.active]},
        {'setting': ['directory'],
         'value': [dir_input.text]},
        {'setting': ['warning'],
         'value': [warn_switch.active]},
        {'setting': ['theme'],
         'value': [theme_input.text]},
        {'setting': ['notifications'],
         'value': [notifications_switch.active]},
        {'setting': ['warn_settings'],
         'value': [ask_switch.active]},
        {'setting': ['save_down_proc'],
         'value': [download_save_switch.active]},
        {'setting': ['beep_finish'],
         'value': [beep_finish_switch.active]},
        {'setting': ['beep_error'],
         'value': [beep_error_switch.active]}
    ]}
    if now_values == original:
        return True
    elif now_values != original:
        return False


def restore_default_settings_query():
    pop = PopupBox(title="Restore Defaults", essence="central", bg_color=get_sub_theme_color("string"))

    box = FloatLayout()
    box.add_widget(Image(source="Assets/Media/help.png", size_hint=(None, None), size=(50, 50),
                         pos_hint={'x': 0, 'y': .4}))
    box.add_widget(
        Label(text="Confirm: Restore Defaults?", pos_hint={'x': .45, 'y': .5}, size_hint=(None, None), width=dp(100),
              height=dp(40), font_size=30, bold=True))

    box.add_widget(
        Label(text="This action is irreversible", pos_hint={'x': .45, 'y': .35}, size_hint=(None, None), width=dp(100),
              height=dp(40), font_size=20))

    box.add_widget(Button(text="Cancel", on_press=lambda obj: pop.exit(), size_hint=(None, None), height=dp(25),
                          pos_hint={'x': 0, 'y': 0}, background_normal="", background_color="#FF5356"))

    box.add_widget(Button(text="Restore", on_press=lambda obj: restore_default_settings(), background_color="#0976FF",
                          background_normal="", height=dp(25), pos_hint={'x': .79, 'y': 0}, size_hint=(None, None),
                          on_release=lambda obj: pop.exit()))

    pop.content(content=box)
    pop.pop()


def restore_default_settings():
    SnackBar(essence="info", message="Restored default settings", bg_color=get_sub_theme_color("tuple"))

    int_switch.active = p.KeyMatch().match("internet_validation")
    valid_switch.active = p.KeyMatch().match("link_validation")
    conc_input.text = str(p.KeyMatch().match("concurrency_limit"))
    approve_switch.active = p.KeyMatch().match("approval")
    dir_input.text = p.KeyMatch().match("directory")
    warn_switch.active = p.KeyMatch().match("warning")
    theme_input.text = p.KeyMatch().match("theme")
    notifications_switch.active = p.KeyMatch().match("notifications")
    ask_switch.active = p.KeyMatch().match("warn_settings")
    download_save_switch.active = p.KeyMatch().match("save_down_proc")
    beep_finish_switch.active = p.KeyMatch().match("beep_finish")
    beep_error_switch.active = p.KeyMatch().match("beep_error")
    p.KeyMatch().load_defaults()


def save_new_settings_query():
    if not affirm_settings():
        if p.KeyMatch().match("warn_settings"):
            save_new_settings_popup()
        elif not p.KeyMatch().match("warn_settings"):
            save_new_settings()
    elif affirm_settings():
        pass


def save_new_settings():
    SnackBar(essence="info", message="New Settings Saved", bg_color=get_sub_theme_color("tuple"))
    dictionary = {'preferences': [
        {'setting': ['internet_validation'],
         'value': [int_switch.active]},
        {'setting': ['link_validation'],
         'value': [valid_switch.active]},
        {'setting': ['concurrency_limit'],
         'value': [conc_input.text]},
        {'setting': ['approval'],
         'value': [approve_switch.active]},
        {'setting': ['directory'],
         'value': [dir_input.text]},
        {'setting': ['warning'],
         'value': [warn_switch.active]},
        {'setting': ['theme'],
         'value': [theme_input.text]},
        {'setting': ['notifications'],
         'value': [notifications_switch.active]},
        {'setting': ['warn_settings'],
         'value': [ask_switch.active]},
        {'setting': ['save_down_proc'],
         'value': [download_save_switch.active]},
        {'setting': ['beep_finish'],
         'value': [beep_finish_switch.active]},
        {'setting': ['beep_error'],
         'value': [beep_error_switch.active]}
    ]}
    p.KeyMatch().load(dictionary)


def save_new_settings_popup():
    pop_save = PopupBox(title="Save settings", essence="central", bg_color=get_main_theme_color("string"))

    pop_box = FloatLayout()
    pop_box.add_widget(Image(source="Assets/Media/help.png", size_hint=(None, None), size=(50, 50),
                             pos_hint={'x': 0, 'y': .4}))
    pop_box.add_widget(Label(text="Confirm: Save new settings?", pos_hint={'x': .45, 'y': .5}, size_hint=(None, None),
                             width=dp(100), height=dp(40), font_size=30, bold=True))

    pop_box.add_widget(
        Button(text="Cancel", on_press=lambda obj: pop_save.exit(), background_color="#FF5356", size_hint=(None, None),
               height=dp(25), pos_hint={'x': 0, 'y': 0}, background_normal="", on_release=lambda obj: load_settings()))

    pop_box.add_widget(
        Button(text="Save", on_press=lambda obj: save_new_settings(), background_color="#0976FF",
               background_normal="", pos_hint={'x': .79, 'y': 0}, on_release=lambda obj: pop_save.exit(), height=dp(25),
               size_hint=(None, None)))

    pop_save.content(content=pop_box)
    importlib.reload(p)
    pop_save.pop()


def load_settings():
    int_switch.active = p.KeyMatch().match("internet_validation")
    valid_switch.active = p.KeyMatch().match("link_validation")
    conc_input.text = str(p.KeyMatch().match("concurrency_limit"))
    approve_switch.active = p.KeyMatch().match("approval")
    dir_input.text = p.KeyMatch().match("directory")
    warn_switch.active = p.KeyMatch().match("warning")
    theme_input.text = p.KeyMatch().match("theme")
    notifications_switch.active = p.KeyMatch().match("notifications")
    ask_switch.active = p.KeyMatch().match("warn_settings")
    download_save_switch.active = p.KeyMatch().match("save_down_proc")
    beep_finish_switch.active = p.KeyMatch().match("beep_finish")
    beep_error_switch.active = p.KeyMatch().match("beep_error")


def cancel_new_settings():
    importlib.reload(p)
    SnackBar(essence="info", message="New Settings not saved.", bg_color=get_sub_theme_color("tuple"))

    int_switch.active = p.KeyMatch().match("internet_validation")
    valid_switch.active = p.KeyMatch().match("link_validation")
    conc_input.text = str(p.KeyMatch().match("concurrency_limit"))
    approve_switch.active = p.KeyMatch().match("approval")
    dir_input.text = p.KeyMatch().match("directory")
    warn_switch.active = p.KeyMatch().match("warning")
    theme_input.text = p.KeyMatch().match("theme")
    notifications_switch.active = p.KeyMatch().match("notifications")
    ask_switch.active = p.KeyMatch().match("warn_settings")
    download_save_switch.active = p.KeyMatch().match("save_down_proc")
    beep_finish_switch.active = p.KeyMatch().match("beep_finish")
    beep_error_switch.active = p.KeyMatch().match("beep_error")
