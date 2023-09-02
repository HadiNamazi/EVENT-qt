# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from . import simple_report_search as srs

name = ''
unpacked_count = ''
packed_count = ''
sr = None

class Ui_Form(object):

    def ok_click(self):
        srs.s.close()

    def updater(self):
        self.unpacked_lbl.setText(unpacked_count)
        self.packed_lbl.setText(packed_count)
        self.name_lbl.setText('گزارش موجودی {}'.format(name))

    def setupUi(self, Form):
        global sr
        sr = self
        Form.setObjectName("Form")
        Form.setFixedSize(394, 142)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(60, 50, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(240, 50, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.ok_btn = QtWidgets.QPushButton(Form)
        self.ok_btn.clicked.connect(self.ok_click)############
        self.ok_btn.setGeometry(QtCore.QRect(160, 100, 81, 23))
        self.ok_btn.setObjectName("ok_btn")
        self.unpacked_lbl = QtWidgets.QLabel(Form)
        self.unpacked_lbl.setGeometry(QtCore.QRect(190, 50, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.unpacked_lbl.setFont(font)
        self.unpacked_lbl.setStyleSheet("color:#c80000")
        self.unpacked_lbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.unpacked_lbl.setObjectName("unpacked_lbl")
        self.packed_lbl = QtWidgets.QLabel(Form)
        self.packed_lbl.setGeometry(QtCore.QRect(10, 50, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.packed_lbl.setFont(font)
        self.packed_lbl.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.packed_lbl.setStyleSheet("color:#00aa00")
        self.packed_lbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.packed_lbl.setObjectName("packed_lbl")
        self.name_lbl = QtWidgets.QLabel(Form)
        self.name_lbl.setGeometry(QtCore.QRect(10, 10, 371, 20))
        self.name_lbl.setStyleSheet("color:#444444")
        self.name_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.name_lbl.setObjectName("name_lbl")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "گزارش بر اساس نام کالا"))
        self.label.setText(_translate("Form", "بسته بندی شده :"))
        self.label_2.setText(_translate("Form", "بسته بندی نشده :"))
        self.ok_btn.setText(_translate("Form", "OK"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
