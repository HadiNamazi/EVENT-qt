import sqlite3
from PyQt5.QtWidgets import QMessageBox

# to connect to sqlite and have a cursor
con = sqlite3.connect("db.db", check_same_thread=False)
cur = con.cursor()

def history_tracker(history):
    unpacked = 0
    packed = 0
    sold = 0
    defective = 0
    unpacked_returned = 0

    for i in history:
        if i[3] == '01':
            unpacked += int(i[1])
        elif i[3] == '12':
            if int(i[1]) > unpacked:
                return False
            unpacked -= int(i[1])
            packed += int(i[1])
        elif i[3] == '23':
            if int(i[1]) > packed:
                return False
            packed -= int(i[1])
            sold += int(i[1])
        elif i[3][2] == '0':  # kasri
            if i[3][0] == '1':
                if int(i[1]) > unpacked:
                    return False
                unpacked -= int(i[1])
            if i[3][0] == '2':
                if int(i[1]) > packed:
                    return False
                packed -= int(i[1])
            if i[3][0] == '3':
                if int(i[1]) > sold:
                    return False
                sold -= int(i[1])
        elif i[3][2] == '1':  # mazad
            if i[3][0] == '1':
                unpacked += int(i[1])
            elif i[3][0] == '2':
                packed += int(i[1])
            elif i[3][0] == '3':
                sold += int(i[1])
        elif i[3][2] == '2':  # defective
            if int(i[1]) > unpacked:
                return False
            unpacked -= int(i[1])
            defective += int(i[1])
        elif i[3][2] == '2':  # returned_unpacked
            if int(i[1]) > defective:
                return False
            unpacked -= int(i[1])
            unpacked_returned += int(i[1])
    return True

def history_limiter(history, name):
    # filtering history by name
    limited_history = []
    for i in history:
        if i[0] == name:
            limited_history.append(i)
    return limited_history

def date_to_int(date):
    return int(date.replace('/', ''))

#______________________________________________global usage______________________________________________

def check_conflict(history, name=None):
    if name is not None:
        limited_history = history_limiter(history, name)
        return history_tracker(limited_history)
    else:
        names = cur.execute("SELECT name FROM t1").fetchall()
        for name in names:
            limited_history = history_limiter(history, name[0])
            if not history_tracker(limited_history):
                return False
        return True
    
def date_validator(date):
    splitted_date_str = date.split('/')
    splitted_date = [int(i) for i in splitted_date_str]

    if splitted_date[0] > 1400 and splitted_date[1] >= 1 and splitted_date[1] <= 12 and splitted_date[2] >= 1:
        if splitted_date[1] <= 6:  # 31day
            if splitted_date[2] <= 31:
                return True
        elif splitted_date[1] >= 7 and splitted_date[2] <= 11:  # 30day
            if splitted_date[2] <= 30:
                return True
        else:  # 29day
            if splitted_date[2] <= 29:
                return True
    return False

def warning_dialog(message):
        dialog = QMessageBox()
        dialog.setText(message)
        dialog.setWindowTitle('خطا')
        dialog.setIcon(QMessageBox.Warning)
        dialog.setStandardButtons(QMessageBox.Ok)
        dialog.exec_()

def date_format_reviser(date):
    splitted_date = date.split('/')
    revised_date = ''
    for d in splitted_date:
        if len(d) == 1:
            d = '0' + d
        revised_date += d + '/'
    return revised_date[:-1]