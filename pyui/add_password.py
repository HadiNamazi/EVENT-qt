# -*- coding: utf-8 -*-

import sqlite3
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

s = None
ss = None

class Ui_Form(object):

    # to connect to sqlite and have a cursor
    con = sqlite3.connect("db.db")
    cur = con.cursor()

    def default(self):
        self.pass_inpt.clear()
        self.pass_repeat_inpt.clear()
        self.show_chck.setChecked(False)
        self.pass_inpt.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pass_repeat_inpt.setEchoMode(QtWidgets.QLineEdit.Password)

    def btn_click(self):
        if self.pass_inpt.text() == self.pass_repeat_inpt.text() and self.pass_inpt.text() != '' and self.pass_repeat_inpt.text() != '':
            self.cur.execute('INSERT INTO t3 VALUES(?)', (self.pass_inpt.text(),))
            self.con.commit()
            dialog = QMessageBox()
            dialog.setText('رمز عبور با موفقیت ثبت شد.')
            dialog.setIcon(QMessageBox.Information)
            dialog.setStandardButtons(QMessageBox.Ok)
            dialog.exec_()
            s.close()
        else:
            dialog = QMessageBox()
            dialog.setText('رمز ها با هم همخوانی ندارند.')
            dialog.setIcon(QMessageBox.Warning)
            dialog.setStandardButtons(QMessageBox.Ok)
            dialog.exec_()

    def show_chch_click(self):
        if self.show_chck.isChecked():
            self.pass_inpt.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.pass_repeat_inpt.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.pass_inpt.setEchoMode(QtWidgets.QLineEdit.Password)
            self.pass_repeat_inpt.setEchoMode(QtWidgets.QLineEdit.Password)

    def setupUi(self, Form):
        global s, ss
        ss = self
        Form.setObjectName("Form")
        Form.setFixedSize(238, 242)
        self.pass_inpt = QtWidgets.QLineEdit(Form)
        self.pass_inpt.setGeometry(QtCore.QRect(40, 60, 161, 31))
        self.pass_inpt.setText("")
        self.pass_inpt.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pass_inpt.setObjectName("pass_inpt")
        self.pass_repeat_inpt = QtWidgets.QLineEdit(Form)
        self.pass_repeat_inpt.setGeometry(QtCore.QRect(40, 110, 161, 31))
        self.pass_repeat_inpt.setText("")
        self.pass_repeat_inpt.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pass_repeat_inpt.setObjectName("pass_repeat_inpt")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(40, 20, 161, 20))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.save_btn = QtWidgets.QPushButton(Form)
        self.save_btn.clicked.connect(self.btn_click)
        self.save_btn.setGeometry(QtCore.QRect(40, 180, 161, 31))
        self.save_btn.setObjectName("save_btn")
        self.show_chck = QtWidgets.QCheckBox(Form)
        self.show_chck.stateChanged.connect(self.show_chch_click)
        self.show_chck.setGeometry(QtCore.QRect(40, 150, 161, 20))
        self.show_chck.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.show_chck.setObjectName("show_chck")

        QtWidgets.QWidget.setTabOrder(self.pass_inpt, self.pass_repeat_inpt)
        QtWidgets.QWidget.setTabOrder(self.pass_repeat_inpt, self.show_chck)
        QtWidgets.QWidget.setTabOrder(self.show_chck, self.save_btn)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "افزودن رمز عبور"))
        self.pass_inpt.setPlaceholderText(_translate("Form", "رمز عبور"))
        self.pass_repeat_inpt.setPlaceholderText(_translate("Form", "تکرار رمز عبور"))
        self.label.setText(_translate("Form", "رمز عبور مورد نظر خود را وارد کنید"))
        self.save_btn.setText(_translate("Form", "ذخیره"))
        self.show_chck.setText(_translate("Form", "نمایش رمز عبور"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
