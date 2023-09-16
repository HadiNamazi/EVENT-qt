# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView, QWidget, QFormLayout
from . import main_window as mw
from . import common_functions as cf

from_date = 0
to_date = 0
name = ''
state = ''
s = None


class Ui_Form(object):

    # to connect to sqlite and have a cursor
    con = sqlite3.connect("db.db")
    cur = con.cursor()

    def row_insert(self, i, row):
        self.cur.execute('SELECT * FROM t2 ORDER BY date')
        res = self.cur.fetchall()
        if res[i][3] == '01':
            self.tableWidget.setItem(row, 0, QTableWidgetItem('ورود کالای بسته بندی نشده'))
        elif res[i][3] == '12':
            self.tableWidget.setItem(row, 0, QTableWidgetItem('انجام بسته بندی'))
        elif res[i][3] == '23':
            self.tableWidget.setItem(row, 0, QTableWidgetItem('فروش'))
        elif len(res[i][3]) == 3 and res[i][3] == '110':
            self.tableWidget.setItem(row, 0, QTableWidgetItem('کسری بسته بندی نشده'))
        elif len(res[i][3]) == 3 and res[i][3] == '220':
            self.tableWidget.setItem(row, 0, QTableWidgetItem('کسری بسته بندی شده'))
        elif len(res[i][3]) == 3 and res[i][3] == '111':
            self.tableWidget.setItem(row, 0, QTableWidgetItem('مازاد بسته بندی نشده'))
        elif len(res[i][3]) == 3 and res[i][3] == '221':
            self.tableWidget.setItem(row, 0, QTableWidgetItem('مازاد بسته بندی شده'))
        elif len(res[i][3]) == 3 and res[i][3][2] == '2':
            self.tableWidget.setItem(row, 0, QTableWidgetItem('معیوب'))
        elif len(res[i][3]) == 3 and res[i][3][2] == '3':
            self.tableWidget.setItem(row, 0, QTableWidgetItem('مرجوع خرید'))
        elif len(res[i][3]) == 3 and res[i][3][2] == '4':
            self.tableWidget.setItem(row, 0, QTableWidgetItem('مرجوع فروش'))
        self.tableWidget.setItem(row, 1, QTableWidgetItem(res[i][0]))
        self.tableWidget.setItem(row, 2, QTableWidgetItem(res[i][1]))
        self.tableWidget.setItem(row, 3, QTableWidgetItem(res[i][2]))
        self.tableWidget.setItem(row, 4, QTableWidgetItem(res[i][5]))
        self.tableWidget.setItem(row, 5, QTableWidgetItem(res[i][4]))

    def add_history_list_items(self):
        # to clear tableWidget
        self.tableWidget.setRowCount(0)

        self.cur.execute('SELECT * FROM t2 ORDER BY date')
        res = self.cur.fetchall()

        if from_date == 0 and name == '' and state == '': # all history
            self.tableWidget.setRowCount(len(res))
            for i in range(0, len(res)):
                self.row_insert(i, i)

        elif from_date == 0 and name == '': # state
            i_list = []
            for i in range(0, len(res)):
                if state == 'بسته بندی نشده' and res[i][3] == '01':
                    i_list.append(i)
                elif state == 'بسته بندی شده' and res[i][3] == '12':
                    i_list.append(i)
                elif state == 'فروخته شده' and res[i][3] == '23':
                    i_list.append(i)
            self.tableWidget.setRowCount(len(i_list))
            for i in range(0, len(i_list)):
                self.row_insert(i_list[i], i)

        elif from_date == 0 and state == '': # name
            i_list = []
            for i in range(0, len(res)):
                if name == res[i][0]:
                    i_list.append(i)
            self.tableWidget.setRowCount(len(i_list))
            for i in range(0, len(i_list)):
                self.row_insert(i_list[i], i)

        elif name == '' and state == '': # date
            i_list = []
            for i in range(0, len(res)):
                this_date = cf.date_format_reviser(res[i][2])
                this_date = int(this_date.replace('/', ''))
                if from_date <= this_date :
                    if this_date <= to_date:
                        i_list.append(i)
                    else:
                        break
            self.tableWidget.setRowCount(len(i_list))
            for i in range(0, len(i_list)):
                self.row_insert(i_list[i], i)

        elif from_date == 0: # name, state
            i_list = []
            for i in range(0, len(res)):
                if name == res[i][0]:
                    if state == 'بسته بندی نشده' and res[i][3] == '01':
                        i_list.append(i)
                    elif state == 'بسته بندی شده' and res[i][3] == '12':
                        i_list.append(i)
                    elif state == 'فروخته شده' and res[i][3] == '23':
                        i_list.append(i)
            self.tableWidget.setRowCount(len(i_list))
            for i in range(0, len(i_list)):
                self.row_insert(i_list[i], i)

        elif name == '': # date, state
            i_list = []
            for i in range(0, len(res)):
                this_date = cf.date_format_reviser(res[i][2])
                this_date = int(this_date.replace('/', ''))
                if from_date <= this_date and this_date <= to_date:         
                    if state == 'بسته بندی نشده' and res[i][3] == '01':
                        i_list.append(i)
                    elif state == 'بسته بندی شده' and res[i][3] == '12':
                        i_list.append(i)
                    elif state == 'فروخته شده' and res[i][3] == '23':
                        i_list.append(i)

            self.tableWidget.setRowCount(len(i_list))
            for i in range(0, len(i_list)):
                self.row_insert(i_list[i], i)

        elif state == '': # name, date
            i_list = []
            for i in range(0, len(res)):
                if name == res[i][0]:
                    this_date = cf.date_format_reviser(res[i][2])
                    this_date = int(this_date.replace('/', ''))
                    if from_date <= this_date and this_date <= to_date:
                        i_list.append(i)

            self.tableWidget.setRowCount(len(i_list))
            for i in range(0, len(i_list)):
                self.row_insert(i_list[i], i)

        else: # all of the options are enabled
            i_list = []
            for i in range(0, len(res)):
                if name == res[i][0]:
                    this_date = cf.date_format_reviser(res[i][2])
                    this_date = int(this_date.replace('/', ''))
                    if from_date <= this_date and this_date <= to_date:
                        if state == 'بسته بندی نشده' and res[i][3] == '01':
                            i_list.append(i)
                        elif state == 'بسته بندی شده' and res[i][3] == '12':
                            i_list.append(i)
                        elif state == 'فروخته شده' and res[i][3] == '23':
                            i_list.append(i)
            self.tableWidget.setRowCount(len(i_list))
            for i in range(0, len(i_list)):
                self.row_insert(i_list[i], i)

    def setupUi(self, Form):
        global s
        s = self
        Form.setObjectName("Form")
        Form.setFixedSize(600, 506)
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setGeometry(QtCore.QRect(0, 0, 601, 511))
        self.tableWidget.setAlternatingRowColors(False)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setRowCount(0)
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(97)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "تاریخچه"))
        self.tableWidget.setHorizontalHeaderLabels(['عملیات', 'اسم کالا', 'تعداد', 'تاریخ', 'شماره فاکتور', 'قیمت'])



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
