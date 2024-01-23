from kivymd.uix.card import MDCard

from kivy.properties import ListProperty
from kivy.lang.builder import Builder

Builder.load_string("""
#:import iffloat kivymd.utils.iffloat

<ScoreListItem>:
    size_hint: 1, None
    radius: dp(20)
    height: dp(50)
    padding: dp(8)
    progress: self.width * (sum(root.score) or 0.001) / app.max_score
    md_bg_color: 0,0,0,0
    md_bg_color2: self.theme_cls.bg_dark
    canvas.before:
        Color:
            rgba: self.md_bg_color2
        RoundedRectangle:
            pos: self.pos
            size: self.width, self.height
            radius: [dp(20)]

        Color:
            rgba: 0,0.7,0,1
        RoundedRectangle:
            pos: (self.x + (self.width - (self.progress or 0))), self.y
            size: self.progress or 100, self.height
            radius: [dp(20)]

    MDLabel:
        text: str(iffloat(sum(root.score)))
        halign: 'center'
    MDSeparator:
        color: self.theme_cls.opposite_bg_dark
        orientation: "vertical"
    MDLabel:
        text: str(iffloat(root.score[0]))
        halign: 'center'
    MDSeparator:
        color: self.theme_cls.opposite_bg_dark
        orientation: "vertical"
    MDLabel:
        text: str(iffloat(root.score[1]))
        halign: 'center'
    MDSeparator:
        color: self.theme_cls.opposite_bg_dark
        orientation: "vertical"
    MDLabel:
        text: str(iffloat(root.score[2]))
        halign: 'center'
    MDFloatLayout:
        id: delete
        size_hint: 0, 0
        MDIconButton:
            icon: "close"
            right: root.right 
            center_y: root.center_y
            on_release:
                root.remove_self()

<ScoreListItemNew>:
    size_hint: 1, None
    radius: dp(20)
    height: dp(50)
    padding: dp(8)
    progress: self.width * (sum(root.score) or 0.001) / app.max_score
    md_bg_color: 0,0,0,0
    md_bg_color2: self.theme_cls.bg_dark
    # orientation: 'vertical'
    canvas.before:
        Color:
            rgba: self.md_bg_color2
        RoundedRectangle:
            pos: self.pos
            size: self.width, self.height
            radius: [dp(20)]

        Color:
            rgba: 0,0.7,0,1
        RoundedRectangle:
            pos: (self.x + (self.width - (self.progress or 0))), self.y
            size: self.progress or 100, self.height
            radius: [dp(20)]
    # MDBoxLayout:
    #     spacing: dp(3)
    MDLabel:
        text: str(iffloat(sum(root.score)))
        halign: 'center'
    MDSeparator:
        color: self.theme_cls.opposite_bg_dark
        orientation: "vertical"
    MDTextField:
        font_size: sp(20)
        size_hint: 1, None
        text_color_normal: 0,0,0,1
        text_color_focus: 0,0,0,1
        font_name: "kivymd/fonts/Roboto-Bold.ttf"
        pos_hint: {'center_y': 0.5}
        text: str(iffloat(root.score[0]))
        halign: 'center'
        input_filter: 'float'
        on_focus:
            if float(self.text) > app.max_scores[0]: self.text = str(app.max_scores[0])
        on_text:
            root.score[0] = float(self.text or 0)
            if float(self.text) < 0: self.text = "0"
    MDSeparator:
        color: self.theme_cls.opposite_bg_dark
        orientation: "vertical"
    MDTextField:
        font_size: sp(20)
        size_hint: 1, None
        text_color_normal: 0,0,0,1
        text_color_focus: 0,0,0,1
        font_name: "kivymd/fonts/Roboto-Bold.ttf"
        pos_hint: {'center_y': 0.5}
        text: str(iffloat(root.score[1]))
        halign: 'center'
        input_filter: 'float'
        on_focus:
            if float(self.text) > app.max_scores[1]: self.text = str(app.max_scores[1])
        on_text:
            root.score[1] = float(self.text or 0)
            if float(self.text) < 0: self.text = "0"
    MDSeparator:
        color: self.theme_cls.opposite_bg_dark
        orientation: "vertical"
    MDTextField:
        font_size: sp(20)
        size_hint: 1, None
        text_color_normal: 0,0,0,1
        text_color_focus: 0,0,0,1
        font_name: "kivymd/fonts/Roboto-Bold.ttf"
        pos_hint: {'center_y': 0.5}
        text: str(iffloat(root.score[2]))
        halign: 'center'
        input_filter: 'float'
        on_focus:
            if float(self.text) > app.max_scores[2]: self.text = str(app.max_scores[2])
        on_text:
            root.score[2] = float(self.text or 0)
            if float(self.text) < 0: self.text = "0"
    MDFloatLayout:
        id: delete
        size_hint: 0, 0
        MDIconButton:
            icon: "close"
            right: root.right 
            center_y: root.center_y
            on_release:
                root.remove_self()
        MDIconButton:
            icon: "check"
            x: root.x
            center_y: root.center_y
            on_release:
                root.add()

""")


class ScoreListItem(MDCard):
    score = ListProperty([0, 0, 0])
    md_bg_color2 = ListProperty([25, 50, 5, 0])

    def on_md_bg_color2(self, _, value):
        if value[3] == 0:
            self.remove_widget(self.ids.delete)

    def remove_self(self):
        self.parent.remove_widget(self)
        del self

    @property
    def total(self):
        return sum(self.score)


class ScoreListItemNew(MDCard):
    score = ListProperty([0, 0, 0])
    md_bg_color2 = ListProperty([25, 50, 5, 0])

    def on_md_bg_color2(self, _, value):
        if value[3] == 0:
            self.remove_widget(self.ids.delete)

    def remove_self(self):
        self.parent.remove_widget(self)
        del self

    def add(self):
        self.parent.add(self.score)
        self.parent.remove_widget(self)
        del self
