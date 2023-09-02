# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3
from . import edit_name_serial_search as enss
from PyQt5.QtWidgets import QMessageBox

old_name = ''
old_serial = ''
s = None

class Ui_Form(object):

    # to connect to sqlite and have a cursor
    con = sqlite3.connect("db.db")
    cur = con.cursor()

    def check_name_availability(self, name):
        if name == old_name:
            return False
        if name == '':
            return True
        self.cur.execute("SELECT name FROM t1")
        names = self.cur.fetchall()
        for i in names:
            if i[0] == name:
                return True
        return False

    def check_serial_availability(self, serial):
        if serial == old_serial:
            return False
        if serial == '':
            return True
        self.cur.execute("SELECT serial FROM t1")
        serials = self.cur.fetchall()
        for i in serials:
            if i[0] == serial:
                return True
        return False

    def dialog_clicked(self, dbutton):
        if dbutton.text() == 'OK':
            data1 = (self.name_inpt.text(), old_name)
            data2 = (self.name_inpt.text(), self.serial_inpt.text(), old_name)
            self.cur.execute("UPDATE t2 SET name=? WHERE name=?", data1)
            self.cur.execute("UPDATE t1 SET name=?, serial=? WHERE name=?", data2)
            self.con.commit()
            enss.Ui_Form.search_recommendation(enss.s)

    def btn_clicked(self):
        if not (self.check_name_availability(self.name_inpt.text()) or self.check_serial_availability(self.serial_inpt.text())):
            dialog = QMessageBox()
            dialog.setText('موراد ویرایش شده در تمام تاریخچه کالای مورد نظر اعمال خواهد شد.\nاز ویرایش اطلاعات کالای مورد نظر مطمئن هستید؟')
            dialog.setWindowTitle('Edit warning')
            dialog.setIcon(QMessageBox.Warning)
            dialog.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            dialog.buttonClicked.connect(self.dialog_clicked)
            dialog.exec_()
        else:
            dialog = QMessageBox()
            dialog.setText('نام یا کد وارد شده تکراری میباشد.')
            dialog.setWindowTitle('Edit warning')
            dialog.setIcon(QMessageBox.Information)
            dialog.setStandardButtons(QMessageBox.Ok)
            dialog.exec_()

    def update_input_txts(self):
        self.name_inpt.setText(old_name)
        self.serial_inpt.setText(old_serial)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setFixedSize(393, 120)
        global s
        s = self
        self.name_inpt = QtWidgets.QLineEdit(Form)
        self.name_inpt.setGeometry(QtCore.QRect(20, 20, 251, 31))
        self.name_inpt.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.name_inpt.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.name_inpt.setClearButtonEnabled(True)
        self.name_inpt.setObjectName("name_inpt")
        self.serial_inpt = QtWidgets.QLineEdit(Form)
        self.serial_inpt.setGeometry(QtCore.QRect(280, 20, 91, 31))
        self.serial_inpt.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.serial_inpt.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.serial_inpt.setClearButtonEnabled(True)
        self.serial_inpt.setObjectName("serial_inpt")
        self.edit_btn = QtWidgets.QPushButton(Form)
        self.edit_btn.clicked.connect(self.btn_clicked)
        self.edit_btn.setGeometry(QtCore.QRect(20, 70, 351, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.edit_btn.setFont(font)
        self.edit_btn.setObjectName("edit_btn")

        QtWidgets.QWidget.setTabOrder(self.name_inpt, self.serial_inpt)
        QtWidgets.QWidget.setTabOrder(self.serial_inpt, self.edit_btn)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "ویرایش اسم و کد کالا"))
        self.name_inpt.setPlaceholderText(_translate("Form", "اسم کالا"))
        self.serial_inpt.setPlaceholderText(_translate("Form", "کد کالا"))
        self.edit_btn.setText(_translate("Form", "ویرایش"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
