from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QApplication, QMainWindow, QShortcut
import sys, os
from pyui import main_window, entrance_password
import sqlite3
from pyui import common_functions as cf

if __name__ == "__main__":

    # creating 'Excel exports' folder
    try:
        os.mkdir(cf.resource_path('خروجی های اکسل'))
    except:
        pass

    # to connect to sqlite and have a cursor
    con = sqlite3.connect("db.db")
    cur = con.cursor()

    # to create tables if not exists
    res = cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='t1'")
    if res.fetchone() is None:
        cur.execute("CREATE TABLE t1(name, serial, unpacked_count, packed_count, sold_count, defective_count, min)")
    res = cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='t2'")
    if res.fetchone() is None:
        cur.execute("CREATE TABLE t2(name, count, date, action, price, factor)")
        # action code: - - -
        # (0) -> unpacked(1) -> packed(2) -> sold(3)    *2
        # kasri(0), mazad(1), mayoob(2), marjoo'(3)     *1
    res = cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='t3'")
    if res.fetchone() is None:
        cur.execute("CREATE TABLE t3(password)")
    else:
        res = cur.execute("SELECT password FROM t3").fetchone()
        if res is None:
            # to show entrance_password.py
            app = QApplication(sys.argv)
            win = QMainWindow()
            ui = main_window.Ui_MainWindow()
            ui.setupUi(win)
            win.show()
            sys.exit(app.exec_())
        else:
            # to show main_window.py
            app = QApplication(sys.argv)
            win = QMainWindow()
            ui = entrance_password.Ui_MainWindow()
            ui.setupUi(win)

            win.show()
            app.exec()
