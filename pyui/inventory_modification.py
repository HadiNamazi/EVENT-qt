# -*- coding: utf-8 -*-
import jdatetime
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import sqlite3
from . import main_window as mw
from PyQt5.QtWidgets import QMessageBox
from . import common_functions as cf

s = None

class Ui_Form(object):
    # to connect to sqlite and have a cursor
    con = sqlite3.connect("db.db")
    cur = con.cursor()

    item_text = ''

    def default(self):
        self.name_inpt.clear()
        self.date_inpt.setText(jdatetime.datetime.now().strftime('%Y/%m/%d'))
        self.count_inpt.setValue(1)
        
    def keyboard_selection(self):
        try:
            self.item_text = self.search_list.currentItem().text()
            
            self.name_inpt.textChanged.disconnect()
            self.name_inpt.setText(self.item_text)
            self.name_inpt.textChanged.connect(self.search_recommendation)
        except:
            pass

    def search_recommendation(self):
        self.search_list.clear()
        res = self.cur.execute("SELECT name, serial, unpacked_count, packed_count, sold_count FROM t1").fetchall()

        if self.name_inpt.text() == '':
            rec = []
            for i in res:
                if i[2] != '0':
                    data = i[1] + ' - ' + '(بسته بندی نشده) ' + i[0]
                    rec.append(data)
                if i[3] != '0':
                    data = i[1] + ' - ' + '(بسته بندی شده) ' + i[0]
                    rec.append(data)
                if i[3] != '0':
                    data = i[1] + ' - ' + '(فروخته شده) ' + i[0]
                    rec.append(data)
            self.search_list.addItems(rec)
            self.item_text = ''
        else:
            name = self.name_inpt.text()
            splitted_name = name.split()
            rec = []

            count = 0
            for i in res:
                data1 = i[1] + ' - ' + '(بسته بندی نشده) ' + i[0]
                data2 = i[1] + ' - ' + '(بسته بندی شده) ' + i[0]
                data3 = i[1] + ' - ' + '(فروخته شده) ' + i[0]

                # if one of the items was clicked
                if self.name_inpt.text() == data1:
                    rec = [data1]
                    break
                elif self.name_inpt.text() == data2:
                    rec = [data2]
                    break
                elif self.name_inpt.text() == data3:
                    rec = [data3]
                    break

                for j in splitted_name:
                    if len(splitted_name) == 1 and j in i[1] and not data1 in rec and not data2 in rec and not data3 in rec:
                        if i[2] != '0':
                            data = i[1] + ' - ' + '(بسته بندی نشده) ' + i[0]
                            rec.append(data)
                        if i[3] != '0':
                            data = i[1] + ' - ' + '(بسته بندی شده) ' + i[0]
                            rec.append(data)
                        if i[4] != '0':
                            data = i[1] + ' - ' + '(فروخته شده) ' + i[0]
                            rec.append(data)
                        break
                    if j != '-' and j in i[0] and not data1 in rec and not data2 in rec and not data3 in rec:
                        count += 1
                if count == len(splitted_name):
                    if i[2] != '0':
                        data = i[1] + ' - ' + '(بسته بندی نشده) ' + i[0]
                        rec.append(data)
                    if i[3] != '0':
                        data = i[1] + ' - ' + '(بسته بندی شده) ' + i[0]
                        rec.append(data)
                    if i[4] != '0':
                        data = i[1] + ' - ' + '(فروخته شده) ' + i[0]
                        rec.append(data)
                count = 0

            self.search_list.addItems(rec)


    def item_clicked(self, item):
        self.item_text = item.text()
        self.name_inpt.setText(item.text())

    def btn_clicked(self):
        if self.item_text != '' and self.count_inpt.text() != '' and cf.date_validator(self.date_inpt.text()):
            name = self.item_text.split(')', 1)[1][1:]
            pack = self.item_text.split(')', 1)[0].split('(', 1)[1]
            self.date_inpt.setText(cf.date_format_reviser(self.date_inpt.text()))

            res = self.cur.execute('SELECT unpacked_count, packed_count, defective_count, sold_count FROM t1 WHERE name=?', (name,)).fetchone()

            if self.combo.currentText() == 'کسری':
                if pack == 'بسته بندی نشده':
                    data1 = (str(int(res[0])-int(self.count_inpt.text())), name,)
                    data2 = (name, self.count_inpt.text(), self.date_inpt.text(), '110', None, None,)
                    self.cur.execute('INSERT INTO t2 VALUES(?, ?, ?, ?, ?, ?)', data2)
                    ordered_res = self.cur.execute("SELECT * FROM t2 ORDER BY date").fetchall()
                    if cf.check_conflict(ordered_res, name):
                        self.cur.execute('UPDATE t1 SET unpacked_count=? WHERE name=?', data1)
                        self.con.commit()
                        mw.Ui_MainWindow.status_lbl(mw.s)
                    else:
                        self.con.rollback()
                        cf.warning_dialog('با انجام این عملیات در تاریخچه مشکل ایجاد خواهد شد.')
                elif pack == 'بسته بندی شده':
                    data1 = (str(int(res[1]) - int(self.count_inpt.text())), name,)
                    data2 = (name, self.count_inpt.text(), self.date_inpt.text(), '220', None, None,)
                    self.cur.execute('INSERT INTO t2 VALUES(?, ?, ?, ?, ?, ?)', data2)
                    ordered_res = self.cur.execute("SELECT * FROM t2 ORDER BY date").fetchall()
                    if cf.check_conflict(ordered_res, name):
                        self.cur.execute('UPDATE t1 SET packed_count=? WHERE name=?', data1)
                        self.con.commit()
                        mw.Ui_MainWindow.status_lbl(mw.s)
                    else:
                        self.con.rollback()
                        cf.warning_dialog('با انجام این عملیات در تاریخچه مشکل ایجاد خواهد شد.')
                else:
                    cf.warning_dialog('روی کالای فروخته شده نمی توان کسری اعمال کرد.')
            elif self.combo.currentText() == 'مازاد':
                if pack == 'بسته بندی نشده':
                    data1 = (str(int(res[0]) + int(self.count_inpt.text())), name,)
                    data2 = (name, self.count_inpt.text(), self.date_inpt.text(), '111', None, None,)
                    self.cur.execute('UPDATE t1 SET unpacked_count=? WHERE name=?', data1)
                    self.cur.execute('INSERT INTO t2 VALUES(?, ?, ?, ?, ?, ?)', data2)
                    self.con.commit()
                    mw.Ui_MainWindow.status_lbl(mw.s)
                elif pack == 'بسته بندی شده':
                    data1 = (str(int(res[1]) + int(self.count_inpt.text())), name,)
                    data2 = (name, self.count_inpt.text(), self.date_inpt.text(), '221', None, None,)
                    self.cur.execute('UPDATE t1 SET packed_count=? WHERE name=?', data1)
                    self.cur.execute('INSERT INTO t2 VALUES(?, ?, ?, ?, ?, ?)', data2)
                    self.con.commit()
                    mw.Ui_MainWindow.status_lbl(mw.s)
                else:
                    cf.warning_dialog('روی کالای فروخته شده نمی توان مازاد اعمال کرد.')
            elif self.combo.currentText() == 'معیوب':
                if pack == 'بسته بندی نشده':
                    data1 = (str(int(res[0])-int(self.count_inpt.text())), str(int(res[2])+int(self.count_inpt.text())), name,)
                    data2 = (name, self.count_inpt.text(), self.date_inpt.text(), '112', None, None,)
                    self.cur.execute('INSERT INTO t2 VALUES(?, ?, ?, ?, ?, ?)', data2)
                    ordered_res = self.cur.execute("SELECT * FROM t2 ORDER BY date").fetchall()
                    if cf.check_conflict(ordered_res, name):
                        self.cur.execute('UPDATE t1 SET unpacked_count=?, defective_count=? WHERE name=?', data1)
                        self.con.commit()
                        mw.Ui_MainWindow.status_lbl(mw.s)
                    else:
                        self.con.rollback()
                        cf.warning_dialog('با انجام این عملیات در تاریخچه مشکل ایجاد خواهد شد.')
                else:
                    cf.warning_dialog('فقط کالای بسته بندی نشده میتواند به عنوان کالای معیوب ثبت شود.')

            self.item_text = ''
            
        else:
            cf.warning_dialog('اطلاعات وارد شده معتبر نیست.')

        self.default()


    def setupUi(self, Form):
        global s
        s = self
        Form.setObjectName("Form")
        Form.setFixedSize(600, 506)
        self.name_inpt = QtWidgets.QLineEdit(Form)
        self.name_inpt.textChanged.connect(self.search_recommendation)
        self.name_inpt.setGeometry(QtCore.QRect(40, 30, 221, 31))
        self.name_inpt.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.name_inpt.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.name_inpt.setClearButtonEnabled(True)
        self.name_inpt.setObjectName("name_inpt")
        self.count_inpt = QtWidgets.QSpinBox(Form)
        self.count_inpt.setGeometry(QtCore.QRect(270, 30, 91, 31))
        self.count_inpt.setMinimum(1)
        self.count_inpt.setMaximum(1000000)
        self.count_inpt.setProperty("value", 1)
        self.count_inpt.setObjectName("count_inpt")
        self.date_inpt = QtWidgets.QLineEdit(Form)
        self.date_inpt.setText(jdatetime.datetime.now().strftime('%Y/%m/%d'))
        self.date_inpt.setGeometry(QtCore.QRect(370, 30, 91, 31))
        self.date_inpt.setObjectName("date_inpt")
        self.search_list = QtWidgets.QListWidget(Form)
        self.search_list.currentRowChanged.connect(self.keyboard_selection)
        self.search_list.itemClicked.connect(self.item_clicked)
        self.search_list.setGeometry(QtCore.QRect(40, 80, 521, 351))
        self.search_list.setViewMode(QtWidgets.QListView.ListMode)
        self.search_list.setObjectName("search_list")
        self.add_btn = QtWidgets.QPushButton(Form)
        self.add_btn.clicked.connect(self.btn_clicked)
        self.add_btn.setGeometry(QtCore.QRect(40, 450, 521, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.add_btn.setFont(font)
        self.add_btn.setObjectName("add_btn")
        self.combo = QtWidgets.QComboBox(Form)
        self.combo.setGeometry(QtCore.QRect(470, 30, 91, 31))
        self.combo.setObjectName("combo")
        self.combo.addItem("")
        self.combo.addItem("")
        self.combo.addItem("")
        QtWidgets.QWidget.setTabOrder(self.name_inpt, self.search_list)
        QtWidgets.QWidget.setTabOrder(self.search_list, self.count_inpt)
        QtWidgets.QWidget.setTabOrder(self.count_inpt, self.date_inpt)
        QtWidgets.QWidget.setTabOrder(self.date_inpt, self.combo)
        QtWidgets.QWidget.setTabOrder(self.combo, self.add_btn)

        self.search_recommendation()
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "اصلاح موجودی"))
        self.name_inpt.setPlaceholderText(_translate("Form", "اسم یا کد کالا"))
        self.date_inpt.setPlaceholderText(_translate("Form", "تاریخ"))
        self.add_btn.setText(_translate("Form", "ثبت"))
        self.combo.setItemText(0, _translate("Form", "کسری"))
        self.combo.setItemText(1, _translate("Form", "مازاد"))
        self.combo.setItemText(2, _translate("Form", "معیوب"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
