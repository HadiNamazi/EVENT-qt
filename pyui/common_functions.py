import sqlite3

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
        if i[4] == '01':
            unpacked += int(i[2])
        elif i[4] == '12':
            if int(i[2]) > unpacked:
                return False
            unpacked -= int(i[2])
            packed += int(i[2])
        elif i[4] == '23':
            if int(i[2]) > packed:
                return False
            packed -= int(i[2])
            sold += int(i[2])
        elif i[4][2] == '0':  # kasri
            if i[4][0] == '1':
                if int(i[2]) > unpacked:
                    return False
                unpacked -= int(i[2])
            if i[4][0] == '2':
                if int(i[2]) > packed:
                    return False
                packed -= int(i[2])
            if i[4][0] == '3':
                if int(i[2]) > sold:
                    return False
                sold -= int(i[2])
        elif i[4][2] == '1':  # mazad
            if i[4][0] == '1':
                unpacked += int(i[2])
            elif i[4][0] == '2':
                packed += int(i[2])
            elif i[4][0] == '3':
                sold += int(i[2])
        elif i[4][2] == '2':  # defective
            if int(i[2]) > unpacked:
                return False
            unpacked -= int(i[2])
            defective += int(i[2])
        elif i[4][2] == '2':  # returned_unpacked
            if int(i[2]) > defective:
                return False
            unpacked -= int(i[2])
            unpacked_returned += int(i[2])
    return True

def history_limiter(history, name):
    # filtering history by name
    limited_history = []
    for i in history:
        if i[1] == name:
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