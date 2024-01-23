from contestant_list_item import ContestantListItem, Contestant
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen
from kivy.lang.builder import Builder
from kivymd.app import MDApp

Builder.load_file('home.kv')
app = MDApp.get_running_app()


class HomeScreen(MDScreen):
    def on_enter(self):
        if 'contestants_list' in self.ids:
            contestants_list = self.ids.contestants_list
            contestants_list.clear_widgets()
            contestants = app.contestants.get_all()
            for con in contestants:
                contestants_list.add_widget(ContestantListItem(contestant=con), 2)

    def on_ids(self, _, ids):
        if 'contestants_list' in ids:
            contestants_list = ids.contestants_list
            contestants_list.clear_widgets()
            contestants = app.contestants.get_all()
            for con in contestants:
                contestants_list.add_widget(ContestantListItem(contestant=con), 2)
        if 'judge_name_field' in ids:
            self.ids.judge_name_field.text = app.judge_name

    def new_contestant(self):
        text_field = MDTextField(hint_text=app.text['name'])
        dialog = MDDialog(type='custom', title=app.text['new contestant'], buttons=[
            MDFlatButton(text=app.text['cancel'], on_release=lambda x: dialog.dismiss()),
            MDRaisedButton(text=app.text['add'], on_release=lambda x: self.add_contestant(text_field.text, dialog)),
        ], content_cls=text_field)
        text_field.halign = 'right'
        dialog.open()

    def add_contestant(self, name, dialog):
        con = Contestant(name=name, score=app.max_scores)
        app.contestants.add_new(con)
        self.ids.contestants_list.add_widget(ContestantListItem(contestant=con), 2)
        dialog.dismiss()

