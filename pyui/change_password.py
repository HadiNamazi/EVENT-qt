# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3
from PyQt5.QtWidgets import QMessageBox

s = None
ss = None

class Ui_Form(object):

    # to connect to sqlite and have a cursor
    con = sqlite3.connect("db.db")
    cur = con.cursor()

    def default(self):
        self.current_pass_inpt.clear()
        self.new_pass_inpt.clear()
        self.new_pass_repeat_inpt.clear()
        self.show_chck.setChecked(False)
        self.new_pass_inpt.setEchoMode(QtWidgets.QLineEdit.Password)
        self.current_pass_inpt.setEchoMode(QtWidgets.QLineEdit.Password)
        self.new_pass_repeat_inpt.setEchoMode(QtWidgets.QLineEdit.Password)

    def btn_click(self):
        self.cur.execute('SELECT password FROM t3')
        current_pass = self.cur.fetchone()[0]
        if self.current_pass_inpt.text() != '' and self.new_pass_inpt.text() != '' and self.new_pass_repeat_inpt.text() != '' and self.current_pass_inpt.text() == current_pass and self.new_pass_inpt.text() == self.new_pass_repeat_inpt.text():
            self.cur.execute('UPDATE t3 SET password=? WHERE password=?', (self.new_pass_inpt.text(), current_pass))
            self.con.commit()
            dialog = QMessageBox()
            dialog.setText('رمز عبور با موفقیت ثبت شد.')
            dialog.setIcon(QMessageBox.Information)
            dialog.setStandardButtons(QMessageBox.Ok)
            dialog.exec_()
            self.current_pass_inpt.clear()
            self.new_pass_inpt.clear()
            self.new_pass_repeat_inpt.clear()
            s.close()
        else:
            dialog = QMessageBox()
            dialog.setText('اطلاعات وارد شده صحیح نیستند.')
            dialog.setIcon(QMessageBox.Warning)
            dialog.setStandardButtons(QMessageBox.Ok)
            dialog.exec_()

    def show_chch_click(self):
        if self.show_chck.isChecked():
            self.current_pass_inpt.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.new_pass_inpt.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.new_pass_repeat_inpt.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.current_pass_inpt.setEchoMode(QtWidgets.QLineEdit.Password)
            self.new_pass_inpt.setEchoMode(QtWidgets.QLineEdit.Password)
            self.new_pass_repeat_inpt.setEchoMode(QtWidgets.QLineEdit.Password)

    def setupUi(self, Form):
        global s, ss
        ss = self
        Form.setObjectName("Form")
        Form.setFixedSize(260, 266)
        self.new_pass_inpt = QtWidgets.QLineEdit(Form)
        self.new_pass_inpt.setGeometry(QtCore.QRect(51, 80, 161, 31))
        self.new_pass_inpt.setText("")
        self.new_pass_inpt.setEchoMode(QtWidgets.QLineEdit.Password)
        self.new_pass_inpt.setObjectName("new_pass_inpt")
        self.current_pass_inpt = QtWidgets.QLineEdit(Form)
        self.current_pass_inpt.setGeometry(QtCore.QRect(51, 30, 161, 31))
        self.current_pass_inpt.setText("")
        self.current_pass_inpt.setEchoMode(QtWidgets.QLineEdit.Password)
        self.current_pass_inpt.setObjectName("current_pass_inpt")
        self.new_pass_repeat_inpt = QtWidgets.QLineEdit(Form)
        self.new_pass_repeat_inpt.setGeometry(QtCore.QRect(51, 130, 161, 31))
        self.new_pass_repeat_inpt.setText("")
        self.new_pass_repeat_inpt.setEchoMode(QtWidgets.QLineEdit.Password)
        self.new_pass_repeat_inpt.setObjectName("new_pass_repeat_inpt")
        self.save_btn = QtWidgets.QPushButton(Form)
        self.save_btn.clicked.connect(self.btn_click)
        self.save_btn.setGeometry(QtCore.QRect(51, 200, 161, 31))
        self.save_btn.setObjectName("save_btn")
        self.show_chck = QtWidgets.QCheckBox(Form)
        self.show_chck.stateChanged.connect(self.show_chch_click)
        self.show_chck.setGeometry(QtCore.QRect(50, 170, 161, 20))
        self.show_chck.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.show_chck.setObjectName("show_chck")

        QtWidgets.QWidget.setTabOrder(self.current_pass_inpt, self.new_pass_inpt)
        QtWidgets.QWidget.setTabOrder(self.new_pass_inpt, self.new_pass_repeat_inpt)
        QtWidgets.QWidget.setTabOrder(self.new_pass_repeat_inpt, self.show_chck)
        QtWidgets.QWidget.setTabOrder(self.show_chck, self.save_btn)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "تغییر رمز عبور"))
        self.new_pass_inpt.setPlaceholderText(_translate("Form", "رمز عبور جدید"))
        self.current_pass_inpt.setPlaceholderText(_translate("Form", "رمز عبور فعلی"))
        self.new_pass_repeat_inpt.setPlaceholderText(_translate("Form", "تکرار رمز عبور جدید"))
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
