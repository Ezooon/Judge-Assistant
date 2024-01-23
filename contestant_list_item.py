from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.utils import iffloat
from kivymd.uix.list import ThreeLineIconListItem
from kivymd.uix.card import MDCard
from kivymd.app import MDApp

from kivy.properties import ObjectProperty, StringProperty
from kivy.lang.builder import Builder

from contestant import Contestant

app = MDApp.get_running_app()
Builder.load_string("""
#:import iffloat kivymd.utils.iffloat

<ContestantListItem>:
    halign: 'right'
    text: self.contestant.name
    secondary_text: str(sum(self.contestant.score)) + "/" + str(sum(app.max_scores))
    tertiary_text: root.scores
    theme_text_color: "Custom"
    secondary_theme_text_color: "Custom"
    font_name: "assets/languages/Amiri-Regular.ttf"
    theme_font_styles: 'custom'
    text_color: self.theme_cls.primary_dark
    secondary_text_color: self.theme_cls.primary_color[:3] + [0.76]
    on_release:
        app.root.ids.score_keeping.set_contestant(root.contestant)
        app.root.current = 'score_keeping'

    IconLeftWidget:
        icon: "book-open-variant"
        pos_hint: {'center_y': .5, 'left': 1}
        theme_text_color: 'Custom'
        icon_color: self.theme_cls.primary_color
        on_release:
            app.root.ids.score_keeping.set_contestant(root.contestant)
            app.root.current = 'score_keeping'

    IconLeftWidget:
        icon: "account-remove-outline"
        pos_hint: {'center_y': .5, 'left': .9}
        theme_text_color: 'Custom'
        icon_color: self.theme_cls.primary_color
        on_press:
            root.delete_contestant()
    
    # IconLeftWidget:
    #     icon: "card-account-details-outline"
    #     pos_hint: {'center_y': .5, 'left': .8}
    #     theme_text_color: 'Custom'
    #     icon_color: self.theme_cls.primary_color


<ContestantDetailedScore>:
    halign: 'right'
    size_hint: 1, None
    ripple_behavior: True
    radius: 0
    height: dp(50)
    md_bg_color: 0,0,0,0 
    padding: [dp(10), 0, dp(10), 0]
    orientation: 'vertical'
    canvas.before:
        Color:
            rgba: self.theme_cls.primary_dark
        Rectangle:
            pos: self.x + dp(4), self.y
            size: self.width - dp(8), dp(1)

    MDLabel:
        text: root.contestant.name
        pos_hint: {'center_y': .5, 'left': .9}
        theme_text_color: 'Custom'
        font_size: sp(18)
        font_name: "assets/languages/Amiri-Regular.ttf"
        color: self.theme_cls.primary_color
        halign: 'right'
        shorten: True
        shorten_from: 'left'

    MDBoxLayout:
        size_hint: None, 0.5
        width: dp(172)
        MDLabel:
            text: str(iffloat(sum(root.contestant.score))) + "  |"
            # size_hint: None, 1
            # width: dp(30)
            halign: 'center'
            pos_hint: {'center_y': .5, 'left': .9}
            theme_text_color: 'Custom'
            color: self.theme_cls.primary_color
    
        MDLabel:
            text: str(iffloat(root.contestant.score[2])) + "  |"
            # size_hint: None, 1
            # width: dp(30)
            halign: 'center'
            pos_hint: {'center_y': .5, 'left': .9}
            theme_text_color: 'Custom'
            color: self.theme_cls.primary_color
    
        MDLabel:
            text: str(iffloat(root.contestant.score[1])) + "  |"
            # size_hint: None, 1
            # width: dp(30)
            halign: 'center'
            pos_hint: {'center_y': .5, 'left': .9}
            theme_text_color: 'Custom'
            color: self.theme_cls.primary_color
    
        MDLabel:
            text: str(iffloat(root.contestant.score[0]))
            # size_hint: None, 1
            # width: dp(30)
            halign: 'center'
            pos_hint: {'center_y': .5, 'left': .9}
            theme_text_color: 'Custom'
            color: self.theme_cls.primary_color

""")


class ContestantDetailedScore(MDCard):
    contestant = ObjectProperty(Contestant())

    def on_release(self):
        self.parent.screen.add(self.contestant.score)


class ContestantListItem(ThreeLineIconListItem):
    contestant = ObjectProperty(Contestant())
    scores = StringProperty("")

    def __init__(self, **kwargs):
        super(ContestantListItem, self).__init__(**kwargs)
        self.contestant.bind(score=self.string_scores)
        self.string_scores(None, self.contestant.score)

    def string_scores(self, _, sl):
        ms = app.max_scores
        scores = ''
        for i in range(3):
            scores += str(iffloat(sl[i])) + "/" + str(ms[i]) + "   "
        self.scores = scores[:-3]

    def delete_contestant(self):
        dialog = MDDialog(type='alert', title=app.text['delete contestant'], buttons=[
            MDFlatButton(text=app.text['cancel'], on_release=lambda x: dialog.dismiss()),
            MDRaisedButton(text=app.text['delete'], on_release=lambda x: self.delete(dialog)),
        ])
        dialog.open()

    def delete(self, dialog):
        dialog.dismiss()
        app.contestants.delete(self.contestant.id)
        self.parent.remove_widget(self)
        del self
