from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder

Builder.load_string(
    """
<Card>:
    orientation: "horizontal"
    size_hint: (1, None)
    height: dp(40)
    canvas.before:
        Color:
            rgb: root.color
        Rectangle:
            size: self.size
            pos: self.pos


 """
)


class Card(BoxLayout):
    color = (1, 1, 1)
    pass
