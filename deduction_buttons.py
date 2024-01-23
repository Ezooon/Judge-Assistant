from kivy.properties import NumericProperty
from kivymd.uix.button import MDFillRoundFlatButton
from kivy.lang.builder import Builder

Builder.load_string("""
<DeductionButton>:
    font_size: sp(19)
    MDFloatLayout:
        MDLabel:
            text: str(root.count)
            center: root.right - dp(10), root.top - dp(10)
            size_hint: None, None
            size: dp(25), dp(25)
            color: 1, 1, 1, 1
            bold: True
            font_style: 'Subtitle2'
            font_size: sp(12)
            halign: 'center'
            valign: 'middle'
            canvas.before:
                Color:
                    rgba: 1, 0, 0, 1
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [dp(50)]
""")


class DeductionButton(MDFillRoundFlatButton):
    count = NumericProperty(0)
