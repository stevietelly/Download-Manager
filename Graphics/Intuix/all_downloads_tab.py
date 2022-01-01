from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivymd.material_resources import dp

all_downloads_bg = BoxLayout(orientation="vertical")

top = BoxLayout(size_hint=(1, .07), orientation="horizontal")

top.add_widget(
    Label(text="All Downloads", size_hint=(None, None), width=dp(200), height=dp(40), font_size=20, valign="bottom",
          font_name="Assets/Fonts/Roboto-Light.ttf", pos_hint={"x": 0, "y": 0}))

all_downloading = Button(text="Downloading", size_hint=(None, None), width=dp(150), height=dp(40),
                         pos_hint={"x": .5, "y": 0})
top.add_widget(all_downloading)

all_paused = Button(text="Paused Downloads", size_hint=(None, None), width=dp(150), height=dp(40),
                    pos_hint={"x": .5, "y": 0})
top.add_widget(all_paused)

all_finished = Button(text="Finished Downloads", size_hint=(None, None), width=dp(150), height=dp(40),
                      pos_hint={"x": .5, "y": 0})
top.add_widget(all_finished)

all_error = Button(text="Error Downloads", size_hint=(None, None), width=dp(150), height=dp(40),
                   pos_hint={"x": .5, "y": 0})
top.add_widget(all_error)

all_label = Label(text="0", font_name="Assets/fonts/FiraCode-Bold.ttf", size_hint=(.1, 1))
top.add_widget(all_label)
all_label.color = (1, 1, 1)
all_label.font_size = dp(15)

bottom = BoxLayout(size_hint=(1, .93))

scroll = ScrollView()
scroll.bar_color = "298AFF"
scroll.bar_width = 5
scroll.do_scroll_y = True

all_downloads_box = BoxLayout(orientation="vertical", size_hint=(1, None))

scroll.add_widget(all_downloads_box)
bottom.add_widget(scroll)

all_downloads_bg.add_widget(top)
all_downloads_bg.add_widget(bottom)
