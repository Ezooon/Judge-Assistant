from os import path

from json import load, dump

from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.screenmanager import MDScreenManager

from kivy.properties import StringProperty, ListProperty, DictProperty, NumericProperty, ObjectProperty
from kivy.core.window import Window
from kivy.utils import platform

from contestant import ContestantsApiConnection

root_path = ''
if platform == 'android':
    from android.storage import primary_external_storage_path
    from android.permissions import request_permissions, Permission
    Window.softinput_mode = 'below_target'

    root_path = primary_external_storage_path()


class Screens(MDScreenManager):
    pass


class JudgeAssistant(MDApp):
    contestants = ObjectProperty(ContestantsApiConnection())

    text = DictProperty('')

    judge_name = StringProperty("")

    max_scores = ListProperty([25, 70, 5])
    # the total score is the sum of
    # intonation, memorizing, and performance respectively.

    intonation_deductions = ListProperty([0.2]*5)
    # the score deduction in the case of making the following mistakes
    # Qalqala, Guna, Exit, or Mdd respectively.
    # the last is to revert a deduction

    memorizing_deductions = ListProperty([0.5, 1, 2, 2, 0.5])
    # the score deduction in the case of making the following mistakes
    # a mistake, two, and three mistakes and had to be helped.
    # next value is for being silent for 10 sec.
    # the last is to revert a deduction

    silence_time = NumericProperty(10)
    # the max time a contestant is allowed to be silent

    @property
    def max_score(self):
        return sum(self.max_scores)

    def build_config(self, config):
        config.setdefaults('Judge', {'name': 'حكم 1'})
        config.setdefaults('Score', {'intonation': '25', 'memorizing': '70', 'performance': '5'})
        config.setdefaults('Intonation', {'qalqala': '0.2', 'guna': '0.2', 'exit': '0.2', 'mdd': '0.2',
                                          'revert': '2.0'})
        config.setdefaults('Memorizing', {'mistake': '0.5', 'two': '1.0', 'three': '2', 'silence': '2',
                                          'revert': '0.5', 'silence_time': '10'})

    def save_settings(self):
        config = self.config
        config.set('Judge', 'name', self.judge_name)

        config.set('Score', 'intonation', self.max_scores[0])
        config.set('Score', 'memorizing', self.max_scores[1])
        config.set('Score', 'performance', self.max_scores[2])

        config.set('Intonation', 'qalqala', self.intonation_deductions[0])
        config.set('Intonation', 'guna', self.intonation_deductions[1])
        config.set('Intonation', 'exit', self.intonation_deductions[2])
        config.set('Intonation', 'mdd', self.intonation_deductions[3])
        config.set('Intonation', 'revert', self.intonation_deductions[4])

        config.set('Memorizing', 'mistake', self.memorizing_deductions[0])
        config.set('Memorizing', 'two', self.memorizing_deductions[1])
        config.set('Memorizing', 'three', self.memorizing_deductions[2])
        config.set('Memorizing', 'silence', self.memorizing_deductions[3])
        config.set('Memorizing', 'revert', self.memorizing_deductions[4])

        config.set('Memorizing', 'silence_time', self.silence_time)
        config.write()

    def build(self):
        self.icon = 'icon.ico'
        if platform == 'android':
            request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])

        self.theme_cls.primary_palette = "Brown"
        self.theme_cls.accent_palette = "Amber"

        # load language
        with open('assets/languages/text.json', 'r', encoding="utf8") as f:
            self.text = load(f)
        # load settings
        config = self.config
        self.judge_name = config.get('Judge', 'name')

        self.max_scores[0] = config.getint('Score', 'intonation')
        self.max_scores[1] = config.getint('Score', 'memorizing')
        self.max_scores[2] = config.getint('Score', 'performance')

        self.intonation_deductions[0] = config.getfloat('Intonation', 'qalqala')
        self.intonation_deductions[1] = config.getfloat('Intonation', 'guna')
        self.intonation_deductions[2] = config.getfloat('Intonation', 'exit')
        self.intonation_deductions[3] = config.getfloat('Intonation', 'mdd')
        self.intonation_deductions[4] = config.getfloat('Intonation', 'revert')

        self.memorizing_deductions[0] = config.getfloat('Memorizing', 'mistake')
        self.memorizing_deductions[1] = config.getfloat('Memorizing', 'two')
        self.memorizing_deductions[2] = config.getfloat('Memorizing', 'three')
        self.memorizing_deductions[3] = config.getfloat('Memorizing', 'silence')
        self.memorizing_deductions[4] = config.getfloat('Memorizing', 'revert')

        self.silence_time = config.getint('Memorizing', 'silence_time')
        self.save_settings()
        return Screens()

    def export(self):
        file_text = {'settings': dict()}
        file_text["settings"]['Score'] = self.config.items('Score')
        file_text["settings"]['Intonation'] = self.config.items('Intonation')
        file_text["settings"]['Memorizing'] = self.config.items('Memorizing')
        file_text["contestants"] = self.contestants.get_all_export()
        with open(path.join(root_path, 'judge_assistant_backup.json'), 'w', encoding='utf8') as f:
            dump(file_text, f, indent=4, ensure_ascii=False)
        toast(f'تم توريد المتسابقين إلي {root_path} يمكنك الأن مشاركته')

    def import_(self):
        if path.exists(path.join(root_path, 'judge_assistant_backup.json')):
            with open(path.join(root_path, 'judge_assistant_backup.json'), 'r', encoding='utf8') as f:
                file_text = load(f)
            print(file_text)
        else:
            toast(f'لم يتم إيجاد ملف إعدادات في {"root"}')


JudgeAssistant().run()


# Todo better to export the settings with the contestants.
#   Adam's change requests:
#       higher contrast in colors.
#       DONE# one click to play the alarm noise.
