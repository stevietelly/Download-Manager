from kivy.uix.button import Button
from kivy.lang.builder import Builder

Builder.load_string(
"""
<FlatButton>:
    background_normal: ""
    size_hint: (None, 1)
    width: dp(100)
    color: "000000"
"""
)


class FlatButton(Button):
    pass
