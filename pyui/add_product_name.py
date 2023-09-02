# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3
from . import main_window as mw

s = None

class Ui_Form(object):

    def default(self):
        self.name_inpt.clear()
        self.serial_inpt.clear()

    def check_name_availability(self, name):
        if name == '':
            return True
        # connecting to sqlite and have a cursor
        con = sqlite3.connect("db.db")
        cur = con.cursor()
        cur.execute("SELECT name FROM t1")
        names = cur.fetchall()
        for i in names:
            if i[0] == name:
                return True
        return False

    def check_serial_availability(self, serial):
        if serial == '':
            return True
        # connecting to sqlite and have a cursor
        con = sqlite3.connect("db.db")
        cur = con.cursor()
        cur.execute("SELECT serial FROM t1")
        serials = cur.fetchall()
        for i in serials:
            if i[0] == serial:
                return True
        return False

    def clicked(self):
        if (not self.check_name_availability(self.name_inpt.text())) and (not self.check_serial_availability(self.serial_inpt.text())):
            # removing the error label
            self.error_lbl.setText('')
            # connecting to sqlite and have a cursor
            con = sqlite3.connect("db.db")
            cur = con.cursor()
            # inserting name and serial to t1
            name = self.name_inpt.text().replace('\n', '')
            data = (name, self.serial_inpt.text(), '0', '0', '0', '0', None)
            cur.execute("INSERT INTO t1 VALUES(?, ?, ?, ?, ?, ?, ?)", data)
            con.commit()
            mw.Ui_MainWindow.status_lbl(mw.s)
            # to clear the inputs
            self.name_inpt.clear()
            self.serial_inpt.clear()
        else:
            self.error_lbl.setText('نام یا سریال کالای مورد نظر موجود می باشد')

    def setupUi(self, Form):
        global s
        s = self
        Form.setObjectName("Form")
        Form.setFixedSize(422, 125)
        self.name_inpt = QtWidgets.QLineEdit(Form)
        self.name_inpt.setGeometry(QtCore.QRect(20, 30, 211, 31))
        self.name_inpt.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.name_inpt.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.name_inpt.setClearButtonEnabled(True)
        self.name_inpt.setObjectName("name_inpt")
        self.add_btn = QtWidgets.QPushButton(Form)
        self.add_btn.clicked.connect(self.clicked)
        self.add_btn.setGeometry(QtCore.QRect(330, 30, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.add_btn.setFont(font)
        self.add_btn.setObjectName("add_btn")
        self.error_lbl = QtWidgets.QLabel(Form)
        self.error_lbl.setGeometry(QtCore.QRect(40, 80, 361, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.error_lbl.setFont(font)
        self.error_lbl.setStyleSheet("color: #E32800")
        self.error_lbl.setText("")
        self.error_lbl.setObjectName("error_lbl")
        self.serial_inpt = QtWidgets.QLineEdit(Form)
        self.serial_inpt.setGeometry(QtCore.QRect(240, 30, 81, 31))
        self.serial_inpt.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.serial_inpt.setText("")
        self.serial_inpt.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.serial_inpt.setClearButtonEnabled(True)
        self.serial_inpt.setObjectName("serial_inpt")

        QtWidgets.QWidget.setTabOrder(self.name_inpt, self.serial_inpt)
        QtWidgets.QWidget.setTabOrder(self.serial_inpt, self.add_btn)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "افزودن اسم و کد کالا"))
        self.name_inpt.setPlaceholderText(_translate("Form", "اسم کالا"))
        self.add_btn.setText(_translate("Form", "ثبت"))
        self.serial_inpt.setPlaceholderText(_translate("Form", "کد کالا"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
