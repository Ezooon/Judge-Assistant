from kivy.metrics import dp
from kivymd.app import MDApp
from kivy.animation import Animation
from kivy.lang.builder import Builder
from kivymd.uix.screen import MDScreen
from kivy.properties import ListProperty
from score_item_list import ScoreListItem
from contestant_list_item import ContestantDetailedScore
Builder.load_file('compare.kv')
app = MDApp.get_running_app()


class Compare(MDScreen):
    avg_score = ListProperty([0, 0, 0])

    def recalculate_avg(self, items):
        totals = [0, 0, 0]
        items_number = len(items)
        for item in items:
            if not isinstance(item, ScoreListItem):
                items_number -= 1
                continue

            for i in range(3):
                totals[i] += item.score[i]

        for i in range(3):
            self.avg_score[i] = totals[i] / (items_number or 1)

    def drawer(self, button):
        contestants = self.ids.contestants
        if contestants.x == self.right:
            Animation(x=self.width - contestants.width - dp(5), d=.3).start(contestants)
            Animation(x=self.width - contestants.width - dp(5), d=.3).start(button)
            return
        Animation(x=self.right, d=.3).start(contestants)
        Animation(right=self.right - dp(5), d=.3).start(button)

    def on_enter(self):
        if 'contestants_list' in self.ids:
            contestants_list = self.ids.contestants_list
            contestants_list.clear_widgets()
            contestants = app.contestants.get_all()
            for con in contestants:
                contestants_list.add_widget(ContestantDetailedScore(contestant=con), 2)

    def on_ids(self, _, ids):
        if 'contestants_list' in ids:
            contestants_list = ids.contestants_list
            contestants_list.clear_widgets()
            contestants = app.contestants.get_all()
            for con in contestants:
                contestants_list.add_widget(ContestantDetailedScore(contestant=con), 2)

    def add(self, score):
        self.ids.scores_box.add_widget(ScoreListItem(score=score), 1)

    def on_touch_down(self, touch):
        super(Compare, self).on_touch_down(touch)
        contestants = self.ids.contestants
        if not contestants.collide_point(*touch.pos):
            Animation(x=self.right, d=.3).start(contestants)
