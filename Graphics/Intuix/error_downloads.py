from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivymd.material_resources import dp

error_bg = BoxLayout(orientation="vertical")

top = BoxLayout(size_hint=(1, .07), orientation="horizontal")

top.add_widget(
    Label(text="Error Downloads", size_hint=(None, None), width=dp(200), height=dp(40), font_size=20, valign="bottom",
          font_name="Assets/Fonts/Roboto-Light.ttf", pos_hint={"x": 0, "y": 0}))

error_all = Button(text="All Downloads", size_hint=(None, None), width=dp(150), height=dp(40),
                   pos_hint={"x": .5, "y": 0})
top.add_widget(error_all)

error_downloading = Button(text="Downloading", size_hint=(None, None), width=dp(150), height=dp(40),
                           pos_hint={"x": .5, "y": 0})
top.add_widget(error_downloading)

error_finished = Button(text="Finished Downloads", size_hint=(None, None), width=dp(150), height=dp(40),
                        pos_hint={"x": .5, "y": 0})
top.add_widget(error_finished)

error_paused = Button(text="Paused Downloads", size_hint=(None, None), width=dp(150), height=dp(40),
                      pos_hint={"x": .5, "y": 0})
top.add_widget(error_paused)

error_label = Label(text="0", font_name="Assets/fonts/FiraCode-Bold.ttf", size_hint=(.1, 1), color=(1, 1, 1),
                    font_size=dp(15))
top.add_widget(error_label)

bottom = BoxLayout(size_hint=(1, .93))

scroll = ScrollView()

error_box = BoxLayout()

scroll.add_widget(error_box)
bottom.add_widget(scroll)

error_bg.add_widget(top)
error_bg.add_widget(bottom)
