from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivymd.material_resources import dp

downloading_bg = BoxLayout(orientation="vertical")

top = BoxLayout(size_hint=(1, .07), orientation="horizontal")

top.add_widget(
    Label(text="Downloading", size_hint=(None, None), width=dp(200), height=dp(40), font_size=20, valign="bottom",
          font_name="Assets/Fonts/Roboto-Light.ttf", pos_hint={"x": 0, "y": 0}))

downloading_all = Button(text="All Downloads", size_hint=(None, None), width=dp(150), height=dp(40),
                         pos_hint={"x": .5, "y": 0})
top.add_widget(downloading_all)

downloading_paused = Button(text="Paused Downloads", size_hint=(None, None), width=dp(150), height=dp(40),
                            pos_hint={"x": .5, "y": 0})
top.add_widget(downloading_paused)

downloading_finished = Button(text="Finished Downloads", size_hint=(None, None), width=dp(150), height=dp(40),
                              pos_hint={"x": .5, "y": 0})
top.add_widget(downloading_finished)

downloading_error = Button(text="Error Downloads", size_hint=(None, None), width=dp(150), height=dp(40),
                           pos_hint={"x": .5, "y": 0})
top.add_widget(downloading_error)

downloading_label = Label(text="0", font_name="Assets/fonts/FiraCode-Bold.ttf", size_hint=(.1, 1))
top.add_widget(downloading_label)
downloading_label.color = (1, 1, 1)
downloading_label.font_size = dp(15)

bottom = BoxLayout(size_hint=(1, .93))

scroll = ScrollView()

downloading_box = BoxLayout()

scroll.add_widget(downloading_box)
bottom.add_widget(scroll)

downloading_bg.add_widget(top)
downloading_bg.add_widget(bottom)
