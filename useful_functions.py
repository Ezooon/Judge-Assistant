from arabic_reshaper import reshape # يلصق الأحرف
from bidi.algorithm import get_display # يرتب الأحرف


def to_ar(txt):
    txt = str(txt)
    return get_display(reshape(txt))


def list_of_floats(str_float_list):
    float_list = str_float_list[1:len(str_float_list) - 1].split(', ')

    for i in range(len(float_list)):
        float_list[i] = float(float_list[i])

    return float_list


def list_of_ints(str_int_list):
    if str_int_list in ('', None, [], '[]', 'None') or str_int_list.__class__ == list:
        return []

    int_list = str_int_list[1:len(str_int_list) - 1].split(', ')

    for i in range(len(int_list)):
        int_list[i] = int(int_list[i])

    return int_list


def list_of_strs(s_list):
    strin = s_list[1:-1]
    return strin.split(', ')


def db_list_of_strs(s_list):
    strin = s_list[1:-1]
    quoted = strin.split(', ')
    not_quoted = []
    for quote in quoted:
        not_quoted.append(quote[1:-1])
    return not_quoted


def date_list(s):
    from datetime import date
    s = str(s)
    if s == 'None':
        return []
    lst = s.split(', d')
    dates_args = []
    dates = []
    for o in lst:
        start = o.find('(')
        end = o.find(')')
        dates_args.append(list_of_ints('[' + o[start+1:end] + ']'))
    for args in dates_args:
        dates.append(date(args[0], args[1], args[2]))

    return dates


def stbool(t_bool):
    if t_bool == 'False':
        return False
    return True


def useless_zero(int_: int, cells=2):
    int_ = str(int_)
    result = ''
    for i in range(cells-len(int_)):
        result += '0'
    return result + int_


def op_color(color):
    if color is None:
        return [0, 0, 0, 0]
    return [abs(1-color[0]), abs(1-color[1]), abs(1-color[2]), color[3]]


def frist_gap(tuples):
    alist = []
    for tup in tuples:
        alist.append(tup[0])

    for i in range(len(alist)):
        n = i+1
        if n not in alist:
            return n
    return alist.__len__()


def name_list(names):
    length = len(names)
    text = ''
    line = 1
    names.reverse()
    # a line 103 letters
    for name in names:
        if len(text)+len(name) > 103 and line == 1:
            text = '\n' + text
            line = 2
        if len(text)+len(name) > 206 and line == 2:
            text = '\n' + text
            line = 3
        if len(text)+len(name) > 312 and line == 3:
            text = '\n' + text
            line = 4
        if len(text)+len(name) > 415 and line == 4:
            text = '\n' + text
            line = 5
        text = f' {name} '+ ('' if names.index(name) == 0 else '-') + text

    return text


def one_itemed_tuples(tups):
    return [tup[0] for tup in tups]


def fromtimestamp(string):
    # 2021-03-18 22:25:00.612805
    from datetime import date
    string = string[:10]
    date_ = [int(i) for i in string.split('-')]
    return date(*date_)


def ralign(st, width):
    real_width = len(st)
    emptyness = ''
    for c in range(width-real_width):
        emptyness += ' '
    return emptyness + st

