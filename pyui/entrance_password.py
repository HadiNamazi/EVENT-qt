import sqlite3
import threading

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
from . import main_window
import sys
# from pynput import keyboard


class Ui_MainWindow(QMainWindow):

    # to connect to sqlite and have a cursor
    con = sqlite3.connect("db.db", check_same_thread=False)
    cur = con.cursor()

    mainwindow = None
    key_count = 0

    def btn_clicked(self):
        password = self.cur.execute("SELECT password FROM t3").fetchone()[0]
        if password == self.pass_inpt.text():
            # to show main_window.py
            self.app = QApplication(sys.argv)
            self.win = QMainWindow()
            self.ui = main_window.Ui_MainWindow()
            self.ui.setupUi(self.win)
            self.win.show()
            self.app.exec()
        else:
            self.pass_inpt.clear()

    def enter_btn_clicked(self):
        with keyboard.Events() as events:
            for event in events:
                if event.key == keyboard.Key.enter:
                    self.key_count += 1
                    if self.key_count % 2 == 1:
                        self.btn_clicked()


    def setupUi(self, MainWindow):
        self.mainwindow = MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(247, 160)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pass_inpt = QtWidgets.QLineEdit(self.centralwidget)
        self.pass_inpt.setGeometry(QtCore.QRect(50, 55, 141, 23))
        self.pass_inpt.setObjectName("pass_inpt")
        self.pass_inpt.setEchoMode(QtWidgets.QLineEdit.Password)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 20, 141, 20))
        self.label.setObjectName("label")
        self.enter_btn = QtWidgets.QPushButton(self.centralwidget)
        self.enter_btn.clicked.connect(self.btn_clicked)
        self.enter_btn.setGeometry(QtCore.QRect(50, 90, 141, 25))
        self.enter_btn.setObjectName("enter_btn")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 247, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        # thread = threading.Thread(target=self.enter_btn_clicked)
        # thread.start()

        QtWidgets.QWidget.setTabOrder(self.pass_inpt, self.enter_btn)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "رمز عبور"))
        self.label.setText(_translate("MainWindow", "رمز عبور خود را وارد کنید:"))
        self.enter_btn.setText(_translate("MainWindow", "ورود"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
