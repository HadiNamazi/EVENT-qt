# -*- coding: utf-8 -*-
import threading
from . import common_functions as cf
from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3
from PyQt5.QtCore import pyqtSignal
import jdatetime
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QListWidgetItem
from . import main_window as mw
from time import sleep
# from pynput import keyboard

s = None

class KeyboardWidget(QtWidgets.QWidget):
    keyPressed = pyqtSignal(str)

    def keyPressEvent(self, keyEvent):
        self.keyPressed.emit(keyEvent.text())


class Ui_Form(object):

    # to connect to sqlite and have a cursor
    con = sqlite3.connect("db.db")
    cur = con.cursor()

    item_text = ''

    def default(self):
        self.search_list.clear()
        self.name_inpt.clear()
        self.date_inpt.setText(jdatetime.datetime.now().strftime('%Y/%m/%d'))
        self.count_inpt.setValue(1)

    def search_recommendation(self):
        self.search_list.clear()

        if self.name_inpt.text() == '':
            self.cur.execute("SELECT name, serial, unpacked_count FROM t1")
            res = self.cur.fetchall()
            rec = []
            for i in res:
                data = i[1] + ' - ' + i[0]
                rec.append(data)
            for item_text in rec:
                item = QListWidgetItem(item_text)
                self.search_list.addItem(item)
                self.item_text = ''
        else:
            name = self.name_inpt.text()
            splitted_name = name.split()
            rec = []

            self.cur.execute("SELECT name, serial, unpacked_count FROM t1")
            res = self.cur.fetchall()

            count = 0
            for i in res:
                data = i[1] + ' - ' + i[0]
                # if one of the items was clicked
                if self.name_inpt.text() == data:
                    rec = [data]
                    break
                for j in splitted_name:
                    if len(splitted_name) == 1 and j in i[1] and not data in rec:
                        rec.append(data)
                        break
                    if j != '-' and j in i[0] and not data in rec:
                        count += 1
                if count == len(splitted_name):
                    rec.append(data)
                count = 0

            for item_text in rec:
                item = QListWidgetItem(item_text)
                self.search_list.addItem(item)


    def item_clicked(self, item):
        self.item_text = item.text()
        self.name_inpt.setText(item.text())

    def btn_clicked(self):
        self.date_inpt.setText(cf.date_format_reviser(self.date_inpt.text()))
        if self.item_text != '' and self.count_inpt.text() != '' and cf.date_validator(self.date_inpt.text()):
            text_array = self.item_text.split()[2:]
            text = ''
            for t in text_array:
                text += t + ' '
            text = text[0:len(text)-1]
            self.cur.execute("SELECT unpacked_count FROM t1 WHERE name=?", (text,))
            unpacked_count = str(int(self.cur.fetchone()[0]) + int(self.count_inpt.text()))
            data1 = (text, self.count_inpt.text(), self.date_inpt.text(), '01', None, None)
            data2 = (unpacked_count, text)
            self.cur.execute("INSERT INTO t2 VALUES(?, ?, ?, ?, ?, ?)", data1)
            self.cur.execute("UPDATE t1 SET unpacked_count=? WHERE name=?", data2)
            self.con.commit()
            mw.Ui_MainWindow.status_lbl(mw.s)
            self.item_text = ''
        else:
            dialog = QMessageBox()
            dialog.setText('اطلاعات وارد شده معتبر نیست.')
            dialog.setWindowTitle('خطا')
            dialog.setIcon(QMessageBox.Information)
            dialog.setStandardButtons(QMessageBox.Ok)
            dialog.exec_()
        self.name_inpt.clear()
        self.count_inpt.setValue(1)
        self.date_inpt.setText(jdatetime.datetime.now().strftime('%Y/%m/%d'))

    # key_count = 0
    # def keyboard_listener(self):
    #     with keyboard.Events() as events:
    #         for event in events:
    #             if event.key == keyboard.Key.enter:
    #                 self.key_count += 1
    #                 if self.key_count % 2 == 1:
    #                     key_count = (self.key_count+1)/2
    #                     if key_count % 4 == 1:
    #                         self.name_inpt.setFocus()
    #                     elif key_count % 4 == 2:
    #                         self.count_inpt.setFocus()
    #                     elif key_count % 4 == 3:
    #                         self.date_inpt.setFocus()
    #                     else:
    #                         self.search_list.setFocus()

    def setupUi(self, Form):
        global s
        s = self
        Form.setObjectName("Form")
        Form.setFixedSize(600, 506)
        self.name_inpt = QtWidgets.QLineEdit(Form)
        self.name_inpt.textChanged.connect(self.search_recommendation)
        self.name_inpt.setGeometry(QtCore.QRect(40, 30, 321, 31))
        self.name_inpt.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.name_inpt.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.name_inpt.setClearButtonEnabled(True)
        self.name_inpt.setObjectName("name_inpt")
        self.count_inpt = QtWidgets.QSpinBox(Form)
        self.count_inpt.setGeometry(QtCore.QRect(370, 30, 91, 31))
        self.count_inpt.setMinimum(1)
        self.count_inpt.setMaximum(1000000)
        self.count_inpt.setProperty("value", 1)
        self.count_inpt.setObjectName("count_inpt")
        self.search_list = QtWidgets.QListWidget(Form)
        self.search_list.itemClicked.connect(self.item_clicked)
        self.search_list.setGeometry(QtCore.QRect(40, 80, 521, 351))
        self.search_list.setViewMode(QtWidgets.QListView.ListMode)
        self.search_list.setObjectName("search_list")
        self.search_recommendation()
        self.add_btn = QtWidgets.QPushButton(Form)
        self.add_btn.clicked.connect(self.btn_clicked)
        self.add_btn.setGeometry(QtCore.QRect(40, 450, 521, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.add_btn.setFont(font)
        self.add_btn.setObjectName("add_btn")
        self.date_inpt = QtWidgets.QLineEdit(Form)
        self.date_inpt.setText(jdatetime.datetime.now().strftime('%Y/%m/%d'))
        self.date_inpt.setGeometry(QtCore.QRect(470, 30, 91, 31))
        self.date_inpt.setObjectName("date_inpt")
        # thread = threading.Thread(target=self.keyboard_listener)
        # thread.start()
        self.retranslateUi(Form)

        QtWidgets.QWidget.setTabOrder(self.name_inpt, self.search_list)
        QtWidgets.QWidget.setTabOrder(self.search_list, self.count_inpt)
        QtWidgets.QWidget.setTabOrder(self.count_inpt, self.date_inpt)
        QtWidgets.QWidget.setTabOrder(self.date_inpt, self.add_btn)

        # thread = threading.Thread(target=self.mykeypressevent)
        # thread.start()
        # self.date_inpt.setFocus()
        # self.date_inpt.keyPressEvent(Qt.Key_Enter)
        QtCore.QMetaObject.connectSlotsByName(Form)


    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "ثبت ورود کالای بسته بندی نشده"))
        self.name_inpt.setPlaceholderText(_translate("Form", "اسم یا کد کالا"))
        self.add_btn.setText(_translate("Form", "ثبت"))
        self.date_inpt.setPlaceholderText(_translate("Form", "تاریخ"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
