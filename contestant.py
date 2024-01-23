from useful_functions import list_of_ints, list_of_floats
from kivy.properties import StringProperty, ListProperty, NumericProperty
from kivy.uix.widget import EventDispatcher
from sqlite3 import connect


class Contestant(EventDispatcher):
    id = NumericProperty(0)

    name = StringProperty("محمد أحمد خالد علي صالح")

    score = ListProperty([25, 70, 5])
    # the total score is the sum of
    # intonation, memorizing, and performance respectively.

    intonation = ListProperty([0, 0, 0, 0])
    # keeping the number of times the contestant missed a
    # Qalqala, Guna, Exit, or Mdd respectively.

    memorizing = ListProperty([0, 0, 0, 0])
    # keeping the number of times the contestant made
    # a mistake, two, and three mistakes and had to be helped.
    # the last value is the timed they been silence for 10 sec.

    @property
    def total_score(self):
        return sum(self.score)


class ContestantsApiConnection:
    # con for contestant
    # & conn for connection
    def __init__(self):
        self.conn = connect('contestants.db')
        self.cur = self.conn.cursor()

    def add_new(self, con):
        args = [con.name, str(con.score), str(con.intonation), str(con.memorizing)]
        self.cur.execute("""INSERT INTO contestants(name, score, intonation, memorizing) VALUES (?, ?, ?, ?)""", args)
        self.conn.commit()

    def get_all(self):
        self.cur.execute('SELECT * FROM contestants')
        contestants = []
        for con in self.cur.fetchall():
            contestants.append(Contestant(id=con[0], name=con[1], score=list_of_floats(con[2]),
                                          intonation=list_of_ints(con[3]), memorizing=list_of_ints(con[4])))
        return contestants

    def get_all_export(self):
        self.cur.execute('SELECT * FROM contestants')
        contestants = []
        for con in self.cur.fetchall():
            contestants.append({'name': con[1], 'score': con[2],
                                'intonation': con[3], 'memorizing': con[4]})
        return contestants

    def edit(self, con):
        args = (con.name, str(con.score), str(con.intonation), str(con.memorizing), con.id)
        self.cur.execute("""UPDATE contestants SET name = ?, score = ?, intonation = ?, memorizing = ?
                            WHERE id = ?""", args)
        self.conn.commit()

    def delete(self, con_id):
        self.cur.execute('DELETE FROM contestants WHERE "id" = ?', (con_id,))
        self.conn.commit()
