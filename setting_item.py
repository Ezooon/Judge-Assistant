from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel

from kivy.properties import StringProperty, NumericProperty, DictProperty
from kivy.lang.builder import Builder

Builder.load_string("""
<NumericSettingItem>:
    halign: 'right'
    size_hint: 1, None
    radius: 0
    height: dp(50)
    md_bg_color: self.theme_cls.primary_dark
    padding: [dp(10), 0, dp(10), 0]

    IconLeftWidget:
        icon: "plus"
        pos_hint: {'center_y': .5, 'left': 1}
        theme_text_color: 'Custom'
        icon_color: self.theme_cls.bg_normal
        on_press:
            root.plus()

    MDLabel:
        text: str(root.value)
        size_hint: None, 1
        font_size: sp(22)
        font_name: "assets/languages/18 Khebrat Musamim Bold.ttf"
        width: dp(48)
        halign: 'center'
        pos_hint: {'center_y': .5, 'left': .9}
        theme_text_color: 'Custom'
        color: self.theme_cls.bg_normal

    IconLeftWidget:
        icon: "minus"
        pos_hint: {'center_y': .5, 'left': .8}
        theme_text_color: 'Custom'
        icon_color: self.theme_cls.bg_normal
        on_press:
            root.minus()

    MDLabel:
        text: root.name
        font_size: sp(22)
        pos_hint: {'center_y': .5, 'left': .9}
        theme_text_color: 'Custom'
        color: self.theme_cls.bg_normal
        halign: 'right'
        
<SettingCategory>:
    size_hint: 1, None
    height: dp(20)
    halign: 'right'
    padding: [dp(10), 0]
    font_size: sp(19)
    theme_text_color: 'Custom'
    color: self.theme_cls.primary_dark
    canvas.before:
        Color:
            rgba: self.theme_cls.bg_normal
        Rectangle:
            pos: self.pos
            size: self.size

        Color:
            rgba: self.theme_cls.primary_dark
        Rectangle:
            pos: self.x, self.top - dp(1)
            size: self.width, dp(1)
        Color:
            rgba: self.theme_cls.primary_dark
        Rectangle:
            pos: self.pos
            size: self.width, dp(1)
""")
app = MDApp.get_running_app()
SETTINGS = {
    'm_score_i': [app.max_scores, 0, 1, 'intonation total'],
    'm_score_m': [app.max_scores, 1, 1, 'memorizing total'],
    'm_score_p': [app.max_scores, 2, 1, 'performance total'],

    'i_q': [app.intonation_deductions, 0, 0.1, 'qalqala'],
    'i_g': [app.intonation_deductions, 1, 0.1, 'guna'],
    'i_e': [app.intonation_deductions, 2, 0.1, 'exit'],
    'i_m': [app.intonation_deductions, 3, 0.1, 'mdd'],
    'i_r': [app.intonation_deductions, 4, 0.1, 'revert'],

    'm_1': [app.memorizing_deductions, 0, .5, 'mistake'],
    'm_2': [app.memorizing_deductions, 1, .5, '2 mistakes'],
    'm_3': [app.memorizing_deductions, 2, .5, '3 mistakes'],
    'm_s': [app.memorizing_deductions, 3, .5, 'silence'],
    'm_r': [app.memorizing_deductions, 4, .5, 'revert'],

    'silence_time': [[app.silence_time], 0, 1, 'silence length'],
}


class NumericSettingItem(MDCard):
    name = StringProperty("memorizing")
    value = NumericProperty(70)
    accuracy = NumericProperty(1)
    setting = StringProperty()

    def on_setting(self, _, value):
        setting = SETTINGS[value]
        self.value = setting[0][setting[1]]
        self.accuracy = setting[2]
        self.name = app.text[setting[3]]

    def plus(self):
        setting = SETTINGS[self.setting]
        setting[0][setting[1]] = round(setting[0][setting[1]] + self.accuracy, 2)
        value = setting[0][setting[1]]
        self.value = value

    def minus(self):
        setting = SETTINGS[self.setting]
        if setting[0][setting[1]] - self.accuracy > 0:
            setting[0][setting[1]] = round(setting[0][setting[1]] - self.accuracy, 2)
        else:
            setting[0][setting[1]] = 0
        value = setting[0][setting[1]]
        self.value = value


class SettingCategory(MDLabel):
    pass
