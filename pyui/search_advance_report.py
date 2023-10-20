# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3

from PyQt5.QtWidgets import QMessageBox
from . import common_functions as cf
from . import advance_report

s = None

class AdvanceReportForm(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = advance_report.Ui_Form()
        self.ui.setupUi(self)


class Ui_Form(object):
    # to connect to sqlite and have a cursor
    con = sqlite3.connect("db.db")
    cur = con.cursor()

    item_text = ''

    advanceReportForm = None

    def default(self):
        self.name_inpt.clear()
        self.to_date_inpt.clear()
        self.from_date_inpt.clear()
        self.state_chck.setChecked(False)
        self.date_chck.setChecked(False)
        self.product_chck.setChecked(False)

    def keyboard_selection(self):
        try:
            self.item_text = self.search_list.currentItem().text()
            
            self.name_inpt.textChanged.disconnect()
            self.name_inpt.setText(self.item_text)
            self.name_inpt.textChanged.connect(self.search_recommendation)
        except:
            pass

    def advance_report_click(self):
        if not self.advanceReportForm:
            self.advanceReportForm = AdvanceReportForm()
        advance_report.Ui_Form.add_history_list_items(advance_report.s)
        self.advanceReportForm.show()

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

    def date_validator(self, date):
        if date == '':
            return False
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

    def name_extractor(self):
        text_array = self.item_text.split()[2:]
        text = ''
        for t in text_array:
            text += t + ' '
        text = text[0:len(text) - 1]
        return text

    def btn_clicked(self):
        # converting date to int if date checkbox is checked
        t = 1
        f = 2
        if self.date_chck.isChecked() and self.date_validator(self.from_date_inpt.text()) and self.date_validator(
                self.to_date_inpt.text()):
            # adding 0 to date strings
            from_date = cf.date_format_reviser(self.from_date_inpt.text())
            to_date = cf.date_format_reviser(self.to_date_inpt.text())

            f = int(from_date.replace('/', ''))
            t = int(to_date.replace('/', ''))

        # validating input datas
        if self.date_chck.isChecked():
            if not (self.date_validator(self.from_date_inpt.text()) and self.date_validator(
                    self.to_date_inpt.text()) and t >= f):
                dialog = QMessageBox()
                dialog.setText('اطلاعات وارد شده معتبر نیست.')
                dialog.setWindowTitle('خطا')
                dialog.setIcon(QMessageBox.Information)
                dialog.setStandardButtons(QMessageBox.Ok)
                dialog.exec_()
                return
        if self.product_chck.isChecked():
            if self.item_text == '':
                dialog = QMessageBox()
                dialog.setText('اطلاعات وارد شده معتبر نیست.')
                dialog.setWindowTitle('خطا')
                dialog.setIcon(QMessageBox.Information)
                dialog.setStandardButtons(QMessageBox.Ok)
                dialog.exec_()
                return
        if self.state_chck.isChecked():
            if self.state_combo.currentText() == 'بسته بندی نشده':
                if self.product_chck.isChecked():
                    self.cur.execute('SELECT unpacked_count FROM t1 WHERE name=?', (self.name_extractor(),))
                    if self.cur.fetchone()[0] == '0':
                        dialog = QMessageBox()
                        dialog.setText('کالای بسته بندی نشده ای برای این محصول وجود ندارد.')
                        dialog.setWindowTitle('خطا')
                        dialog.setIcon(QMessageBox.Information)
                        dialog.setStandardButtons(QMessageBox.Ok)
                        dialog.exec_()
                        return
            elif self.state_combo.currentText() == 'بسته بندی شده':
                if self.product_chck.isChecked():
                    self.cur.execute('SELECT packed_count FROM t1 WHERE name=?', (self.name_extractor(),))
                    if self.cur.fetchone()[0] == '0':
                        dialog = QMessageBox()
                        dialog.setText('کالای بسته بندی شده ای برای این محصول وجود ندارد.')
                        dialog.setWindowTitle('خطا')
                        dialog.setIcon(QMessageBox.Information)
                        dialog.setStandardButtons(QMessageBox.Ok)
                        dialog.exec_()
                        return
            elif self.state_combo.currentText() == 'فروخته شده':
                if self.product_chck.isChecked():
                    self.cur.execute('SELECT sold_count FROM t1 WHERE name=?', (self.name_extractor(),))
                    if self.cur.fetchone()[0] == '0':
                        dialog = QMessageBox()
                        dialog.setText('کالای فروخته شده ای برای این محصول وجود ندارد.')
                        dialog.setWindowTitle('خطا')
                        dialog.setIcon(QMessageBox.Information)
                        dialog.setStandardButtons(QMessageBox.Ok)
                        dialog.exec_()
                        return

        # if all inputs were ok then:

        advance_report.name = ''
        advance_report.from_date = 0
        advance_report.to_date = 0
        advance_report.state = ''
        if self.product_chck.isChecked():
            advance_report.name = self.name_extractor()
        if self.date_chck.isChecked():
            advance_report.from_date = f
            advance_report.to_date = t
        if self.state_chck.isChecked():
            advance_report.state = self.state_combo.currentText()

        self.advance_report_click()

        self.item_text = ''
        self.name_inpt.clear()

    def product_chck_click(self):
        if self.product_chck.isChecked():
            self.name_inpt.setEnabled(True)
            self.search_list.setEnabled(True)
        else:
            self.name_inpt.setEnabled(False)
            self.search_list.setEnabled(False)

    def date_chck_click(self):
        if self.date_chck.isChecked():
            self.from_date_inpt.setEnabled(True)
            self.to_date_inpt.setEnabled(True)
        else:
            self.from_date_inpt.setEnabled(False)
            self.to_date_inpt.setEnabled(False)

    def state_chck_click(self):
        if self.state_chck.isChecked():
            self.state_combo.setEnabled(True)
        else:
            self.state_combo.setEnabled(False)

    def setupUi(self, Form):
        global s
        s = self
        Form.setObjectName("Form")
        Form.setFixedSize(600, 506)
        self.name_inpt = QtWidgets.QLineEdit(Form)
        self.name_inpt.textChanged.connect(self.search_recommendation)
        self.name_inpt.setEnabled(False)
        self.name_inpt.setGeometry(QtCore.QRect(40, 30, 361, 31))
        self.name_inpt.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.name_inpt.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.name_inpt.setClearButtonEnabled(True)
        self.name_inpt.setObjectName("name_inpt")
        self.from_date_inpt = QtWidgets.QLineEdit(Form)
        self.from_date_inpt.setEnabled(False)
        self.from_date_inpt.setGeometry(QtCore.QRect(40, 70, 91, 31))
        self.from_date_inpt.setText("")
        self.from_date_inpt.setClearButtonEnabled(False)
        self.from_date_inpt.setObjectName("from_date_inpt")
        self.to_date_inpt = QtWidgets.QLineEdit(Form)
        self.to_date_inpt.setEnabled(False)
        self.to_date_inpt.setGeometry(QtCore.QRect(140, 70, 91, 31))
        self.to_date_inpt.setText("")
        self.to_date_inpt.setClearButtonEnabled(False)
        self.to_date_inpt.setObjectName("to_date_inpt")
        self.search_list = QtWidgets.QListWidget(Form)
        self.search_list.currentRowChanged.connect(self.keyboard_selection)
        self.search_list.itemClicked.connect(self.item_clicked)
        self.search_list.setEnabled(False)
        self.search_list.setGeometry(QtCore.QRect(40, 110, 521, 321))
        self.search_list.setViewMode(QtWidgets.QListView.ListMode)
        self.search_list.setObjectName("search_list")
        self.search_btn = QtWidgets.QPushButton(Form)
        self.search_btn.clicked.connect(self.btn_clicked)
        self.search_btn.setGeometry(QtCore.QRect(40, 450, 521, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.search_btn.setFont(font)
        self.search_btn.setObjectName("search_btn")
        self.product_chck = QtWidgets.QCheckBox(Form)
        self.product_chck.stateChanged.connect(self.product_chck_click)
        self.product_chck.setGeometry(QtCore.QRect(410, 30, 121, 17))
        self.product_chck.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.product_chck.setObjectName("product_chck")
        self.date_chck = QtWidgets.QCheckBox(Form)
        self.date_chck.stateChanged.connect(self.date_chck_click)
        self.date_chck.setGeometry(QtCore.QRect(410, 50, 121, 17))
        self.date_chck.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.date_chck.setObjectName("date_chck")
        self.state_chck = QtWidgets.QCheckBox(Form)
        self.state_chck.stateChanged.connect(self.state_chck_click)
        self.state_chck.setGeometry(QtCore.QRect(410, 70, 151, 17))
        self.state_chck.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.state_chck.setObjectName("state_chck")
        self.state_combo = QtWidgets.QComboBox(Form)
        self.state_combo.setEnabled(False)
        self.state_combo.setGeometry(QtCore.QRect(240, 70, 161, 31))
        self.state_combo.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.state_combo.setObjectName("state_combo")
        self.state_combo.addItem("")
        self.state_combo.addItem("")
        self.state_combo.addItem("")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "جستجو"))
        self.name_inpt.setPlaceholderText(_translate("Form", "اسم یا کد کالا"))
        self.from_date_inpt.setPlaceholderText(_translate("Form", "از تاریخ"))
        self.to_date_inpt.setPlaceholderText(_translate("Form", "تا تاریخ"))
        self.search_btn.setText(_translate("Form", "مشاهده تاریخچه"))
        self.product_chck.setText(_translate("Form", "جستجو براساس کالا"))
        self.date_chck.setText(_translate("Form", "جستجو براساس تاریخ"))
        self.state_chck.setText(_translate("Form", "جستجو براساس وضعیت کالا"))
        self.state_combo.setItemText(0, _translate("Form", "بسته بندی نشده"))
        self.state_combo.setItemText(1, _translate("Form", "بسته بندی شده"))
        self.state_combo.setItemText(2, _translate("Form", "فروخته شده"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
