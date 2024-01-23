from kivy.properties import NumericProperty, ObjectProperty
from kivy.lang.builder import Builder
from kivy.core.audio import SoundLoader
from kivy.clock import Clock

from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp

from contestant import Contestant

Builder.load_file('score_keeping.kv')
app = MDApp.get_running_app()


class ScoreKeeping(MDScreen):
    seconds = NumericProperty(10)
    contestant = ObjectProperty(Contestant())

    def __init__(self, **kwargs):
        super(ScoreKeeping, self).__init__(**kwargs)
        self.alarm = SoundLoader.load("assets/Media/BeepBeep.mp3")

    def reset_contestant(self):  # only for the testing
        self.contestant.score = app.max_scores
        self.contestant.intonation = [0, 0, 0, 0]
        self.contestant.memorizing = [0, 0, 0, 0]

    def set_contestant(self, con):
        self.list_contestant = con
        self.contestant.id = con.id
        self.ids.name_field.text = con.name
        self.contestant.name = con.name
        self.contestant.score = con.score
        self.contestant.intonation = con.intonation
        self.contestant.memorizing = con.memorizing

    def save(self):
        app.contestants.edit(self.contestant)
        con = self.contestant
        self.list_contestant.id = con.id
        self.list_contestant.name = con.name
        self.list_contestant.score = con.score
        self.list_contestant.intonation = con.intonation
        self.list_contestant.memorizing = con.memorizing

    def timer_button(self, *_):
        silence_time = app.silence_time
        if self.seconds != silence_time:
            self.reset_timer()
        else:
            self.start_timer()

    def start_timer(self):
        d = 1/self.seconds

        def count_down(_):
            self.seconds -= 1
            self.ids.timer.md_bg_color[0] += d
            self.ids.timer.md_bg_color[1] -= d
            self.ids.timer.text_color = [c + d for c in self.ids.timer.text_color[:3]] + [1]
            if self.seconds <= 0:
                return False

        self.seconds -= 1
        self.ids.timer.md_bg_color[0] += d
        self.ids.timer.md_bg_color[1] -= d
        self.timer = Clock.schedule_interval(count_down, 1)

    def reset_timer(self):
        self.timer.cancel()
        self.ids.timer.md_bg_color = 0, 1, 0, 1
        self.seconds = app.silence_time
