# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3

from PyQt5.QtWidgets import QMessageBox

from . import simple_report

s = None
ss = None

class SimpleReportForm(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = simple_report.Ui_Form()
        self.ui.setupUi(self)

class Ui_Form(object):

    # to connect to sqlite and have a cursor
    con = sqlite3.connect("db.db")
    cur = con.cursor()

    item_text = ''
    simpleReportForm = None

    def default(self):
        self.name_inpt.clear()

    def simple_report_click(self):
        if self.item_text != '':
            text_array = self.item_text.split()[2:]
            text = ''
            for t in text_array:
                text += t + ' '
            text = text[0:len(text) - 1]

            self.cur.execute('SELECT unpacked_count, packed_count FROM t1 WHERE name=?', (text,))
            res = self.cur.fetchone()
            simple_report.unpacked_count = res[0]
            simple_report.packed_count = res[1]
            simple_report.name = text

            if not self.simpleReportForm:
                self.simpleReportForm = SimpleReportForm()
            global s
            s = self.simpleReportForm
            simple_report.Ui_Form.updater(simple_report.sr)
            self.simpleReportForm.show()
        else:
            dialog = QMessageBox()
            dialog.setText('شما هیچ کالایی انتخاب نکرده اید.')
            dialog.setWindowTitle('Error')
            dialog.setIcon(QMessageBox.Warning)
            dialog.setStandardButtons(QMessageBox.Ok)
            dialog.exec_()

    def search_recommendation(self):
        self.search_list.clear()

        if self.name_inpt.text() == '':
            self.cur.execute("SELECT name, serial FROM t1")
            res = self.cur.fetchall()
            rec = []
            for i in res:
                data = i[1] + ' - ' + i[0]
                rec.append(data)
            self.search_list.addItems(rec)
            self.item_text = ''
        else:
            name = self.name_inpt.text()
            splitted_name = name.split()
            rec = []

            self.cur.execute("SELECT name, serial FROM t1")
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

            self.search_list.addItems(rec)

    def item_clicked(self, item):
        self.item_text = item.text()
        self.name_inpt.setText(item.text())

    def setupUi(self, Form):
        global ss
        ss = self
        Form.setObjectName("Form")
        Form.setFixedSize(600, 506)
        self.name_inpt = QtWidgets.QLineEdit(Form)
        self.name_inpt.textChanged.connect(self.search_recommendation)
        self.name_inpt.setGeometry(QtCore.QRect(40, 30, 521, 31))
        self.name_inpt.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.name_inpt.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.name_inpt.setClearButtonEnabled(True)
        self.name_inpt.setObjectName("name_inpt")
        self.edit_btn = QtWidgets.QPushButton(Form)
        self.edit_btn.clicked.connect(self.simple_report_click)
        self.edit_btn.setGeometry(QtCore.QRect(40, 450, 521, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.edit_btn.setFont(font)
        self.edit_btn.setObjectName("edit_btn")
        self.search_list = QtWidgets.QListWidget(Form)
        self.search_list.itemClicked.connect(self.item_clicked)
        self.search_list.setGeometry(QtCore.QRect(40, 80, 521, 351))
        self.search_list.setViewMode(QtWidgets.QListView.ListMode)
        self.search_list.setObjectName("search_list")
        self.search_recommendation()

        QtWidgets.QWidget.setTabOrder(self.name_inpt, self.search_list)
        QtWidgets.QWidget.setTabOrder(self.search_list, self.edit_btn)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "جستجو"))
        self.name_inpt.setPlaceholderText(_translate("Form", "اسم یا کد کالا"))
        self.edit_btn.setText(_translate("Form", "انتخاب"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
